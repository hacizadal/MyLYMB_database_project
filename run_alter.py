import argparse
import csv
import os
import time

import pymysql


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "labpass",
    "database": "schemalab",
    "autocommit": True,
}


def connect():
    return pymysql.connect(**DB_CONFIG)


# Each entry is one schema change that can be tested by this shared runner.
CHANGES = {
    "change-type": "MODIFY COLUMN birth_date DATETIME NOT NULL",
    # Leyla's test: add a normal secondary index to an existing column.
    "add-index": "ADD INDEX idx_username (username)",
}


# The clauses below are deliberately explicit so the experiment records
# which ALTER TABLE algorithm was requested.
ALGO_CLAUSE = {
    "blocking": "",
    "copy": "ALGORITHM=COPY, LOCK=NONE",
    "inplace": "ALGORITHM=INPLACE, LOCK=NONE",
    "nocopy": "ALGORITHM=NOCOPY, LOCK=NONE",
}


def run(change, algorithm, out_path):
    base_sql = CHANGES[change]
    clause = ALGO_CLAUSE[algorithm]
    sql = f"ALTER TABLE user_table {base_sql}"
    if clause:
        sql += f", {clause}"

    print(f"Running: {sql}")

    conn = connect()
    cur = conn.cursor()
    error = ""

    start = time.perf_counter()
    try:
        cur.execute(sql)
    except Exception as exc:
        error = str(exc).replace("\n", " ")
    duration = time.perf_counter() - start

    cur.close()
    conn.close()

    row = {
        "timestamp": time.time(),
        "change": change,
        "algorithm": algorithm,
        "sql": sql,
        "duration_seconds": round(duration, 3),
        "error": error,
    }

    new_file = not os.path.exists(out_path) or os.path.getsize(out_path) == 0
    with open(out_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        if new_file:
            writer.writeheader()
        writer.writerow(row)

    if error:
        print(f"FAILED after {duration:.2f}s: {error}")
    else:
        print(f"OK in {duration:.2f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run and time one MariaDB ALTER TABLE test.")
    parser.add_argument("--change", required=True, choices=CHANGES.keys())
    parser.add_argument("--algorithm", required=True, choices=ALGO_CLAUSE.keys())
    parser.add_argument("--out", default="results_alter.csv")
    args = parser.parse_args()
    run(args.change, args.algorithm, args.out)
