import argparse
import csv
import random
import time
from datetime import datetime

import mariadb


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "labpass",
    "database": "schemalab",
}

CSV_FILE = "workload.csv"


def connect_database():
    try:
        connection = mariadb.connect(**DB_CONFIG)
        print("Connected to MariaDB.")
        return connection
    except mariadb.Error as error:
        print("Could not connect to MariaDB:", error)
        return None


def log_result(operation, latency_ms, status, error="", csv_file=CSV_FILE):
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                datetime.now().isoformat(timespec="milliseconds"),
                operation,
                round(latency_ms, 3),
                status,
                error,
            ]
        )


def run_operation(connection, operation, sql, values=None, csv_file=CSV_FILE):
    cursor = connection.cursor()
    start = time.perf_counter()

    try:
        if values is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, values)

        connection.commit()
        latency_ms = (time.perf_counter() - start) * 1000
        log_result(operation, latency_ms, "success", csv_file=csv_file)
        print(f"{operation} - {latency_ms:.3f} ms")

    except mariadb.Error as error:
        latency_ms = (time.perf_counter() - start) * 1000
        connection.rollback()
        log_result(operation, latency_ms, "error", str(error), csv_file)
        print(f"{operation} failed: {error}")

    finally:
        cursor.close()


def insert_user(connection, csv_file=CSV_FILE):
    number = random.randint(100000, 999999)
    birth_date = "2000-01-01"

    sql = """
        INSERT INTO user_table
        (
            first_name,
            middle_name,
            last_name,
            birth_date,
            email_address,
            phone_number,
            country,
            username,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW())
    """

    values = (
        "Test",
        "Workload",
        "User",
        birth_date,
        f"workload{number}@test.com",
        f"+4915{number}",
        "Germany",
        f"workload_{number}",
    )

    run_operation(connection, "INSERT", sql, values, csv_file)


def update_user(connection, csv_file=CSV_FILE):
    sql = """
        UPDATE user_table
        SET country = 'Updated-Germany'
        WHERE username LIKE 'workload_%'
        ORDER BY id DESC
        LIMIT 1
    """
    run_operation(connection, "UPDATE", sql, csv_file=csv_file)


def delete_user(connection, csv_file=CSV_FILE):
    sql = """
        DELETE FROM user_table
        WHERE username LIKE 'workload_%'
        ORDER BY id ASC
        LIMIT 1
    """
    run_operation(connection, "DELETE", sql, csv_file=csv_file)


def initialise_csv(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "operation", "latency_ms", "status", "error"])


def main(interval_seconds, csv_file):
    initialise_csv(csv_file)

    connection = connect_database()
    if connection is None:
        return

    print("Starting workload...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            insert_user(connection, csv_file)
            update_user(connection, csv_file)
            delete_user(connection, csv_file)
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nWorkload stopped.")
    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Continuous DML workload for the MariaDB ALTER TABLE tests.")
    parser.add_argument(
        "--interval",
        type=float,
        default=0.1,
        help="Seconds to wait between INSERT/UPDATE/DELETE cycles (default: 0.1)",
    )
    parser.add_argument(
        "--out",
        default=CSV_FILE,
        help="CSV file for workload measurements (default: workload.csv)",
    )
    args = parser.parse_args()
    main(args.interval, args.out)
