#!/usr/bin/env python3
"""Fill user_table (and optionally orders) with deterministic synthetic rows.

Rows are produced lazily and inserted in batches, so memory use is constant
whatever --rows is. The same --seed always yields the same data.

    python generate_data.py --rows 100000
    python generate_data.py --rows 1000000 --orders-rows 1000000 --truncate
"""
import argparse
import random
import sys
import time
from datetime import datetime, timedelta

import pymysql

from common import connect

FIRST = ["Amine", "Leyla", "Yasmine", "Mirqe", "Bashah", "Sara", "Omar", "Lina", "Karim", "Nora",
         "Adam", "Maya", "Yusuf", "Ines", "Hugo", "Emma", "Noah", "Lea", "Ali", "Zoe"]
LAST = ["Martin", "Bernard", "Dubois", "Haddad", "Benali", "Schmidt", "Muller", "Rossi", "Garcia",
        "Silva", "Novak", "Kowalski", "Nguyen", "Kim", "Sato", "Ivanov", "Costa", "Lopez"]
COUNTRIES = ["Germany", "France", "Morocco", "Spain", "Italy", "Portugal", "Belgium", "Netherlands",
             "Poland", "Sweden", "Norway", "Canada", "Brazil", "Japan", "Egypt", "Turkey"]
DOMAINS = ["mail.com", "test.org", "uni.edu", "post.net"]
STATUSES = ["new", "paid", "shipped", "done", "cancelled"]
BASE_DATE = datetime(2026, 1, 1)   # fixed reference date -> reproducible output

USER_SQL = ("INSERT INTO user_table (first_name, middle_name, last_name, birth_date, "
            "email_address, phone_number, country, username, created_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
ORDER_SQL = "INSERT INTO orders (user_id, order_total, status, created_at) VALUES (%s, %s, %s, %s)"


def user_row(rng, n):
    first, last = rng.choice(FIRST), rng.choice(LAST)
    middle = rng.choice(FIRST) if rng.random() < 0.3 else None
    birth = (datetime(1950, 1, 1) + timedelta(days=rng.randint(0, 20000))).date()
    email = f"{first[0].lower()}{last.lower()}{n}@{rng.choice(DOMAINS)}"[:30]
    phone = f"+{rng.randint(30, 49)}{rng.randint(10**8, 10**10 - 1)}"
    created = BASE_DATE - timedelta(seconds=rng.randint(0, 5 * 365 * 86400))
    return (first, middle, last, birth, email, phone, rng.choice(COUNTRIES), f"user_{n}", created)


def order_row(rng, min_user, max_user):
    total = round(rng.uniform(1, 2000), 2)
    created = BASE_DATE - timedelta(seconds=rng.randint(0, 3 * 365 * 86400))
    return (rng.randint(min_user, max_user), total, rng.choice(STATUSES), created)


def insert_batched(conn, sql, row_iter, total, batch_size, label):
    """Insert rows from an iterator in batches; one commit per batch."""
    start, done, batch = time.perf_counter(), 0, []
    with conn.cursor() as cur:
        for row in row_iter:
            batch.append(row)
            if len(batch) >= batch_size:
                cur.executemany(sql, batch)   # PyMySQL rewrites this into one multi-row INSERT
                conn.commit()
                done += len(batch)
                batch.clear()
                if (done // batch_size) % 20 == 0:
                    print(f"  {label}: {done:,}/{total:,}", file=sys.stderr)
        if batch:
            cur.executemany(sql, batch)
            conn.commit()
            done += len(batch)
    elapsed = time.perf_counter() - start
    print(f"{label}: inserted {done:,} rows in {elapsed:.1f}s ({done / max(elapsed, 1e-9):,.0f} rows/s)")


def populate(conn, rows, orders_rows=0, batch_size=5000, seed=42, truncate=False):
    conn.autocommit(False)
    rng = random.Random(seed)
    with conn.cursor() as cur:
        if truncate:
            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            cur.execute("TRUNCATE TABLE orders")
            cur.execute("TRUNCATE TABLE user_table")
            cur.execute("SET FOREIGN_KEY_CHECKS=1")
        cur.execute("SELECT COUNT(*) FROM user_table")
        if cur.fetchone()[0] and rows:
            raise SystemExit("user_table is not empty: use --truncate (or run reset_db.py).")
    if rows:
        insert_batched(conn, USER_SQL, (user_row(rng, n) for n in range(1, rows + 1)),
                       rows, batch_size, "user_table")
    if orders_rows:
        with conn.cursor() as cur:
            cur.execute("SELECT MIN(id), MAX(id) FROM user_table")
            lo, hi = cur.fetchone()
        if lo is None:
            raise SystemExit("orders reference user_table: generate users first (--rows > 0).")
        insert_batched(conn, ORDER_SQL, (order_row(rng, lo, hi) for _ in range(orders_rows)),
                       orders_rows, batch_size, "orders")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rows", type=int, required=True, help="rows to insert into user_table")
    p.add_argument("--orders-rows", type=int, default=0, help="rows to insert into orders (default 0)")
    p.add_argument("--batch-size", type=int, default=5000, help="rows per INSERT batch (default 5000)")
    p.add_argument("--seed", type=int, default=42, help="random seed (default 42)")
    p.add_argument("--truncate", action="store_true", help="empty both tables first")
    args = p.parse_args()
    try:
        conn = connect(autocommit=False)
    except pymysql.MySQLError as exc:
        raise SystemExit(f"Cannot connect to MariaDB: {exc}\nIs the container up (docker compose up -d) and .env correct?")
    try:
        populate(conn, args.rows, args.orders_rows, args.batch_size, args.seed, args.truncate)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
