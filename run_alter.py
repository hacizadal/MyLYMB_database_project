import argparse
import csv
import os
import time
import pymysql

def connect():
    return pymysql.connect(
        host="127.0.0.1", port=3306,
        user="root", password="labpass",
        database="schemalab", autocommit=True,
    )

CHANGES = {
    "change-type": "MODIFY COLUMN birth_date DATETIME NOT NULL",
}

ALGO_CLAUSE = {
    "blocking": "",
    "copy": "ALGORITHM=COPY, LOCK=NONE",
}

def run(change, algorithm, out_path):
    base_sql = CHANGES[change]
    clause = ALGO_CLAUSE[algorithm]
    sql = f"ALTER TABLE user_table {base_sql}" + (f", {clause}" if clause else "")

    print(f"Running: {sql}")
    conn = connect()
    cur = conn.cursor()
    error = ""

    t0 = time.time()
    try:
        cur.execute(sql)
    except Exception as e:
        error = str(e).replace("\n", " ")
    duration = time.time() - t0

    conn.close()

    row = {
        "timestamp": time.time(),
        "change": change,
        "algorithm": algorithm,
        "sql": sql,
        "duration_seconds": round(duration, 3),
        "error": error,
    }

    new_file = not os.path.exists(out_path)
    with open(out_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if new_file:
            writer.writeheader()
        writer.writerow(row)
        if error:
          print(f"FAILED after {duration:.2f}s: {error}")
        else:
          print(f"OK in {duration:.2f}s")
          
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--change", required=True, choices=CHANGES.keys())
    ap.add_argument("--algorithm", required=True, choices=ALGO_CLAUSE.keys())
    ap.add_argument("--out", default="results_alter.csv")
    args = ap.parse_args()
    run(args.change, args.algorithm, args.out)