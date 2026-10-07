#!/usr/bin/env python3
"""Run and time ONE ALTER TABLE experiment, appending one row to a results CSV.

While the ALTER runs, a second connection polls information_schema.PROCESSLIST to record
the ALTER's progress (MariaDB `Progress` column) and how many other sessions are waiting
on a lock. A failed ALTER (e.g. MariaDB refusing ALGORITHM=INSTANT) is a *result*, not a
crash: it is recorded with its error code and message.

    python run_alter.py --list
    python run_alter.py --change add-index --algorithm inplace --out results/alter_results.csv
    python run_alter.py --change add-fk-fkchecks-off --algorithm inplace --dry-run

The experiment must start from a freshly reset database (see reset_db.py / sweep.sh).
"""
import argparse
import csv
import sys
import threading
import time
import uuid
from pathlib import Path

import pymysql

from common import connect, utc_now_iso
from experiments import ALGORITHMS, CHANGES, build_alter_sql

FIELDS = ["run_id", "tag", "started_at_utc", "ended_at_utc", "server_version", "dataset_rows",
          "change", "family", "table", "requested_algorithm", "alter_clause", "session_config",
          "sql", "duration_seconds", "status", "errno", "error", "max_progress_pct",
          "max_waiting_sessions", "workload_csv"]


class ProcesslistPoller(threading.Thread):
    """Samples the processlist until stopped. Never raises into the main thread."""

    def __init__(self, alter_conn_id, interval):
        super().__init__(daemon=True)
        self.alter_id, self.interval = alter_conn_id, interval
        self.stop_event = threading.Event()
        self.samples = []      # (utc_iso, alter_state, alter_progress, waiting_sessions)

    def run(self):
        try:
            conn = connect()
        except pymysql.MySQLError:
            return
        try:
            while not self.stop_event.is_set():
                try:
                    with conn.cursor() as cur:
                        cur.execute("SELECT ID, STATE, PROGRESS FROM information_schema.PROCESSLIST")
                        rows = cur.fetchall()
                except pymysql.MySQLError:
                    break
                alter = next((r for r in rows if r[0] == self.alter_id), None)
                waiting = sum(1 for r in rows if r[0] != self.alter_id and r[1] and r[1].startswith("Waiting for"))
                if alter:
                    self.samples.append((utc_now_iso(), alter[1] or "", float(alter[2] or 0), waiting))
                self.stop_event.wait(self.interval)
        finally:
            conn.close()


def count_rows(table):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            return cur.fetchone()[0]
    finally:
        conn.close()


def append_row(path, row):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists() or path.stat().st_size == 0
    if not new_file:
        with open(path, newline="", encoding="utf-8") as fh:
            header = next(csv.reader(fh), [])
        if header != FIELDS:
            raise SystemExit(f"{path} has a different column layout; use a new --out file.")
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        if new_file:
            writer.writeheader()
        writer.writerow(row)


def run(args):
    change = CHANGES[args.change]
    sql = build_alter_sql(args.change, args.algorithm)
    session_config = "; ".join(change.session)
    if args.dry_run:
        for stmt in change.session:
            print(stmt + ";")
        print(sql + ";")
        return 0

    dataset_rows = args.dataset_rows if args.dataset_rows is not None else count_rows(change.table)
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()[0]
        for stmt in change.session:
            cur.execute(stmt)

    poller = ProcesslistPoller(conn.thread_id(), args.poll_interval)
    poller.start()
    print(f"[{version}] {session_config + '; ' if session_config else ''}{sql}")

    status, errno, error = "success", "", ""
    started_at = utc_now_iso()
    start = time.perf_counter()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
    except pymysql.MySQLError as exc:
        status, error = "failure", str(exc).replace("\n", " ")
        errno = exc.args[0] if exc.args and isinstance(exc.args[0], int) else ""
    duration = time.perf_counter() - start
    ended_at = utc_now_iso()
    poller.stop_event.set()
    poller.join(timeout=2)
    conn.close()

    if args.poll_out and poller.samples:
        Path(args.poll_out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.poll_out, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["timestamp_utc", "alter_state", "progress_pct", "waiting_sessions"])
            w.writerows(poller.samples)

    row = {
        "run_id": uuid.uuid4().hex[:8], "tag": args.tag, "started_at_utc": started_at,
        "ended_at_utc": ended_at, "server_version": version, "dataset_rows": dataset_rows,
        "change": args.change, "family": change.family, "table": change.table,
        "requested_algorithm": args.algorithm, "alter_clause": ALGORITHMS[args.algorithm][0],
        "session_config": session_config, "sql": sql, "duration_seconds": round(duration, 3),
        "status": status, "errno": errno, "error": error,
        "max_progress_pct": max((s[2] for s in poller.samples), default=""),
        "max_waiting_sessions": max((s[3] for s in poller.samples), default=0),
        "workload_csv": args.workload or "",
    }
    append_row(args.out, row)
    print(f"{status.upper()} in {duration:.3f}s" + (f" - error {errno}: {error}" if error else ""))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="list available changes and algorithms, then exit")
    p.add_argument("--change", choices=CHANGES.keys())
    p.add_argument("--algorithm", choices=ALGORITHMS.keys())
    p.add_argument("--out", default="results/alter_results.csv", help="results CSV (appended) [results/alter_results.csv]")
    p.add_argument("--tag", default="", help="free label stored in the CSV (e.g. sweep id)")
    p.add_argument("--workload", help="path of the concurrent workload CSV (stored so analyze_results.py can join)")
    p.add_argument("--dataset-rows", type=int, help="rows in the target table (counted automatically if omitted)")
    p.add_argument("--poll-interval", type=float, default=0.25, help="processlist polling period, seconds [0.25]")
    p.add_argument("--poll-out", help="optional CSV with the raw processlist samples")
    p.add_argument("--dry-run", action="store_true", help="print the SQL that would run and exit")
    args = p.parse_args()

    if args.list:
        print("Changes:")
        for name, c in CHANGES.items():
            print(f"  {name:<22} {c.table:<11} {c.alter}\n  {'':<22} {c.description}")
        print("Algorithms:")
        for name, (clause, desc) in ALGORITHMS.items():
            print(f"  {name:<10} {clause or '(none)':<32} {desc}")
        return 0
    if not (args.change and args.algorithm):
        p.error("--change and --algorithm are required (or use --list)")
    try:
        return run(args)
    except pymysql.MySQLError as exc:
        print(f"Infrastructure error (not an experiment result): {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
