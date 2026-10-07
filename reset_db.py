#!/usr/bin/env python3
"""Reset the database to the identical baseline state used before EVERY experiment.

    drop + create tables (schema.sql)  ->  generate deterministic dataset  ->  ANALYZE

    python reset_db.py --rows 100000
    python reset_db.py --rows 1000000 --change add-fk      # also fills `orders`
"""
import argparse
import time

import pymysql

from common import ROOT, connect, run_sql_file
from experiments import CHANGES
from generate_data import populate


def reset(rows, orders_rows, seed, batch_size):
    conn = connect(autocommit=True)
    try:
        run_sql_file(conn, ROOT / "schema.sql")
        populate(conn, rows, orders_rows, batch_size, seed)
        conn.autocommit(True)
        with conn.cursor() as cur:
            for table in ("user_table", "orders"):
                cur.execute(f"ANALYZE TABLE {table}")   # refresh statistics: same start state each time
                cur.fetchall()
    finally:
        conn.close()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rows", type=int, required=True, help="rows in user_table")
    p.add_argument("--orders-rows", type=int, default=None,
                   help="rows in orders (default: --rows if --change needs orders, else 0)")
    p.add_argument("--change", choices=CHANGES.keys(), help="experiment about to run (decides if orders is filled)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--batch-size", type=int, default=5000)
    args = p.parse_args()

    orders_rows = args.orders_rows
    if orders_rows is None:
        orders_rows = args.rows if args.change and CHANGES[args.change].needs_orders else 0

    start = time.perf_counter()
    try:
        reset(args.rows, orders_rows, args.seed, args.batch_size)
    except pymysql.MySQLError as exc:
        raise SystemExit(f"Database error during reset: {exc}\nIs the container up (docker compose up -d) and .env correct?")
    print(f"reset done in {time.perf_counter() - start:.1f}s (user_table={args.rows:,}, orders={orders_rows:,}, seed={args.seed})")


if __name__ == "__main__":
    main()
