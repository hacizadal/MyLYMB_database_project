import mariadb
import time
import csv
import random
from datetime import datetime


# MariaDB connection information
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "labpass",
    "database": "schemalab"
}

# File where workload results will be saved
CSV_FILE = "workload.csv"


# Connect to MariaDB
def connect_database():
    try:
        connection = mariadb.connect(**DB_CONFIG)
        print("Connected to MariaDB.")
        return connection

    except mariadb.Error as error:
        print("Could not connect to MariaDB:", error)
        return None


# Save each operation result to the CSV file
def log_result(operation, latency, status, error=""):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            operation,
            round(latency, 3),
            status,
            error
        ])


# Run a SQL operation and measure how long it takes
def run_operation(connection, operation, sql, values=None):
    cursor = connection.cursor()

    start_time = time.perf_counter()

    try:
        if values is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, values)

        connection.commit()

        latency = (time.perf_counter() - start_time) * 1000

        log_result(
            operation,
            latency,
            "success"
        )

        print(
            operation,
            "-",
            round(latency, 3),
            "ms"
        )

    except mariadb.Error as error:
        latency = (time.perf_counter() - start_time) * 1000

        connection.rollback()

        log_result(
            operation,
            latency,
            "error",
            str(error)
        )

        print(operation, "failed:", error)

    finally:
        cursor.close()


# INSERT a new test user
def insert_user(connection):
    number = random.randint(100000, 999999)

    first_name = "Test"
    middle_name = "Workload"
    last_name = "User"

    birth_date = "2000-01-01"

    email = "workload" + str(number) + "@test.com"
    phone = "+4915" + str(number)
    country = "Germany"
    username = "workload_" + str(number)

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
        first_name,
        middle_name,
        last_name,
        birth_date,
        email,
        phone,
        country,
        username
    )

    run_operation(
        connection,
        "INSERT",
        sql,
        values
    )


# UPDATE one of our test users
def update_user(connection):

    sql = """
        UPDATE user_table
        SET country = 'Updated-Germany'
        WHERE username LIKE 'workload_%'
        ORDER BY id DESC
        LIMIT 1
    """

    run_operation(
        connection,
        "UPDATE",
        sql
    )


# DELETE one of our test users
def delete_user(connection):

    sql = """
        DELETE FROM user_table
        WHERE username LIKE 'workload_%'
        ORDER BY id ASC
        LIMIT 1
    """

    run_operation(
        connection,
        "DELETE",
        sql
    )


def main():

    # Create CSV and write column names
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "operation",
            "latency_ms",
            "status",
            "error"
        ])

    # Connect to database
    connection = connect_database()

    if connection is None:
        return

    print("Starting workload...")
    print("Press Ctrl+C to stop.\n")

    try:

        # Keep generating database activity
        while True:

            insert_user(connection)

            update_user(connection)

            delete_user(connection)

            # Small pause before repeating
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nWorkload stopped.")

    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
