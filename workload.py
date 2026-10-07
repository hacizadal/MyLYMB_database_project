#!/usr/bin/env python3
"""Continuous INSERT / UPDATE / DELETE workload, one latency measurement per statement.

Each worker thread owns one connection (autocommit) and loops:

    INSERT one row  ->  UPDATE one of its own rows (by primary key)
                    ->  DELETE its oldest own row (by primary key, once `--backlog` rows exist)

Only rows inserted by the workload are updated/deleted, always by primary key: the
measured latency reflects lock/DDL interference, not table scans, and threads never
touch each other's rows. The pre-generated dataset is left untouched.

Every statement is logged to CSV (UTC start timestamp, latency, status, error code),
including failures such as lock-wait timeouts. Stop with SIGINT/SIGTERM or --duration.

    python workload.py --out results/workload.csv --threads 2 --interval 0.05
    python workload.py --profile orders --duration 60
"""
import argparse
import collections
import csv
import random
import signal
import statistics
import sys
import threading
import time
from pathlib import Path

import pymysql

from common import connect, utc_now_iso

FIELDS = ["timestamp_utc", "thread", "operation", "latency_ms", "status", "errno", "error", "rows_affected"]
RECONNECT_ERRNOS = {2002, 2003, 2006, 2013, 2055, 1927}   # server gone / connection lost / killed


class UserProfile:
    """Writes to user_table."""
    table = "user_table"

    def __init__(self, rng, thread_id, max_user_id):
        self.rng, self.tid, self.counter = rng, thread_id, 0

    def insert(self):
        self.counter += 1
        n = self.rng.randint(100000, 999999)
        tag = f"wl{self.tid}_{self.counter}_{n}"[:30]
        return ("INSERT INTO user_table (first_name, middle_name, last_name, birth_date, email_address, "
                "phone_number, country, username, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())",
                ("Test", "Workload", "User", "2000-01-01", f"{tag}@test.com"[:30], f"+4915{n}", "Germany", tag))

    def update(self, row_id):
        return "UPDATE user_table SET country = %s WHERE id = %s", ("Updated-Germany", row_id)

    def delete(self, row_id):
        return "DELETE FROM user_table WHERE id = %s", (row_id,)


class OrdersProfile:
    """Writes to orders (child table of the add-fk experiment). Inserted user_ids are valid."""
    table = "orders"

    def __init__(self, rng, thread_id, max_user_id):
        self.rng, self.max_user_id = rng, max_user_id

    def insert(self):
        return ("INSERT INTO orders (user_id, order_total, status, created_at) VALUES (%s,%s,%s,NOW())",
                (self.rng.randint(1, self.max_user_id), round(self.rng.uniform(1, 2000), 2), "new"))

    def update(self, row_id):
        return "UPDATE orders SET status = %s WHERE id = %s", ("paid", row_id)

    def delete(self, row_id):
        return "DELETE FROM orders WHERE id = %s", (row_id,)


PROFILES = {"user_table": UserProfile, "orders": OrdersProfile}


class CsvSink:
    """Thread-safe CSV writer that flushes regularly so a killed run keeps its data."""

    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._file = open(path, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file, lineterminator="\n")
        self._writer.writerow(FIELDS)
        self._lock, self._pending = threading.Lock(), 0

    def write(self, row):
        with self._lock:
            self._writer.writerow(row)
            self._pending += 1
            if self._pending >= 200:
                self._file.flush()
                self._pending = 0

    def close(self):
        with self._lock:
            self._file.close()


class Worker(threading.Thread):
    def __init__(self, tid, args, sink, stop, stats, max_user_id):
        super().__init__(name=f"worker-{tid}", daemon=True)
        self.tid, self.args, self.sink, self.stop_event, self.stats = tid, args, sink, stop, stats
        self.rng = random.Random(args.seed + tid)
        self.profile = PROFILES[args.profile](self.rng, tid, max_user_id)
        self.owned = collections.deque()      # ids of rows this worker inserted and has not deleted
        self.conn = None

    def _open(self):
        self.conn = connect(autocommit=True)
        with self.conn.cursor() as cur:       # waits become measurable errors instead of hanging forever
            cur.execute("SET SESSION lock_wait_timeout=%s", (self.args.lock_timeout,))
            cur.execute("SET SESSION innodb_lock_wait_timeout=%s", (self.args.lock_timeout,))

    def _ensure_connection(self):
        while self.conn is None and not self.stop_event.is_set():
            try:
                self._open()
            except pymysql.MySQLError:
                self.conn = None
                time.sleep(0.5)

    def _execute(self, operation, sql, params):
        """Run one statement, log it, and return (ok, lastrowid)."""
        ts = utc_now_iso()
        start = time.perf_counter()
        status, errno, error, affected, last_id = "success", "", "", 0, None
        try:
            with self.conn.cursor() as cur:
                affected = cur.execute(sql, params)
                last_id = cur.lastrowid
        except pymysql.MySQLError as exc:
            status = "error"
            errno = exc.args[0] if exc.args and isinstance(exc.args[0], int) else ""
            error = str(exc).replace("\n", " ")
            if errno in RECONNECT_ERRNOS:
                try:
                    self.conn.close()
                except Exception:
                    pass
                self.conn = None
        latency_ms = (time.perf_counter() - start) * 1000
        self.sink.write([ts, self.tid, operation, round(latency_ms, 3), status, errno, error, affected])
        self.stats.add(operation, latency_ms, status == "success")
        return status == "success", last_id

    def run(self):
        while not self.stop_event.is_set():
            self._ensure_connection()
            if self.conn is None:
                break
            ok, new_id = self._execute("INSERT", *self.profile.insert())
            if ok and new_id:
                self.owned.append(new_id)
            if self.owned and self.conn is not None:
                self._execute("UPDATE", *self.profile.update(self.rng.choice(self.owned)))
            if len(self.owned) > self.args.backlog and self.conn is not None:
                victim = self.owned.popleft()
                ok, _ = self._execute("DELETE", *self.profile.delete(victim))
                if not ok:
                    self.owned.appendleft(victim)    # retry the same row next cycle
            self.stop_event.wait(self.args.interval)
        if self.conn is not None:
            self.conn.close()


class Stats:
    def __init__(self):
        self._lock = threading.Lock()
        self.data = collections.defaultdict(lambda: {"lat": [], "err": 0})

    def add(self, op, latency_ms, ok):
        with self._lock:
            entry = self.data[op]
            entry["lat"].append(latency_ms)
            entry["err"] += 0 if ok else 1

    def report(self):
        lines = []
        for op in ("INSERT", "UPDATE", "DELETE"):
            entry = self.data.get(op)
            if not entry or not entry["lat"]:
                continue
            lat = sorted(entry["lat"])
            p95 = lat[min(len(lat) - 1, int(0.95 * len(lat)))]
            lines.append(f"{op:<6} n={len(lat):>7} errors={entry['err']:>5} "
                         f"p50={statistics.median(lat):8.2f}ms p95={p95:8.2f}ms max={lat[-1]:9.2f}ms")
        return lines


def fetch_max_user_id():
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(MAX(id), 1) FROM user_table")
            return cur.fetchone()[0]
    finally:
        conn.close()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="results/workload.csv", help="CSV output (overwritten) [results/workload.csv]")
    p.add_argument("--profile", choices=PROFILES.keys(), default="user_table", help="table written to [user_table]")
    p.add_argument("--threads", type=int, default=1, help="concurrent client connections [1]")
    p.add_argument("--interval", type=float, default=0.05, help="pause between cycles per thread, seconds [0.05]")
    p.add_argument("--duration", type=float, default=0, help="stop after N seconds (0 = until SIGINT/SIGTERM) [0]")
    p.add_argument("--backlog", type=int, default=50, help="own rows kept before DELETE starts [50]")
    p.add_argument("--lock-timeout", type=int, default=10, help="session lock_wait_timeout, seconds [10]")
    p.add_argument("--seed", type=int, default=1, help="random seed [1]")
    p.add_argument("--ready-file", help="file created once all connections are open (used by sweep.sh)")
    args = p.parse_args()

    try:
        max_user_id = fetch_max_user_id()
    except pymysql.MySQLError as exc:
        print(f"Cannot reach MariaDB: {exc}", file=sys.stderr)
        return 2

    stop, stats, sink = threading.Event(), Stats(), CsvSink(args.out)
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.set())

    workers = [Worker(i, args, sink, stop, stats, max_user_id) for i in range(args.threads)]
    for w in workers:
        w._open()                      # fail fast if a connection cannot be made
    for w in workers:
        w.start()
    if args.ready_file:
        Path(args.ready_file).write_text(utc_now_iso())
    print(f"workload started: profile={args.profile} threads={args.threads} interval={args.interval}s -> {args.out}",
          file=sys.stderr)

    deadline = time.monotonic() + args.duration if args.duration else None
    while not stop.is_set():
        if deadline and time.monotonic() >= deadline:
            stop.set()
        stop.wait(0.2)
    for w in workers:
        w.join(timeout=args.lock_timeout + 5)
    sink.close()
    print("workload stopped. Summary:", file=sys.stderr)
    for line in stats.report():
        print("  " + line, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
