"""Populate the clean lab table and verify the committed row count."""
from datetime import datetime
from faker import Faker
import mysql.connector

TOTAL_ROWS = 1_000_000
BATCH_SIZE = 1_000


def generate_data():
    connection = mysql.connector.connect(
        host="127.0.0.1", port=3306, user="root",
        password="labpass", database="schemalab",
    )
    cursor = connection.cursor()
    fake = Faker()
    try:
        # Refuse to append to an old experiment's data.
        cursor.execute("SELECT COUNT(*) FROM user_table")
        if cursor.fetchone()[0] != 0:
            raise RuntimeError("user_table is not empty. Run reset_database.py first.")
        insert_query = """
            INSERT INTO user_table
            (first_name, middle_name, last_name, birth_date, email_address,
             phone_number, country, username, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for start in range(0, TOTAL_ROWS, BATCH_SIZE):
            # min also handles a final batch smaller than BATCH_SIZE.
            batch_size = min(BATCH_SIZE, TOTAL_ROWS - start)
            rows = []
            for _ in range(batch_size):
                # Match schema limits, including long phone numbers/country names.
                rows.append((
                    fake.first_name()[:50], fake.first_name()[:50],
                    fake.last_name()[:50], fake.date_of_birth(),
                    fake.email()[:100], fake.phone_number()[:25],
                    fake.country()[:60], fake.user_name()[:30], datetime.now(),
                ))
            cursor.executemany(insert_query, rows)
            connection.commit()
            print(f"Inserted {start + batch_size:,} / {TOTAL_ROWS:,} rows", flush=True)

        # Check the database itself, not just our loop counter.
        cursor.execute("SELECT COUNT(*) FROM user_table")
        actual_rows = cursor.fetchone()[0]
        print(f"Verified user_table row count: {actual_rows:,}", flush=True)
        if actual_rows != TOTAL_ROWS:
            raise RuntimeError(f"Expected {TOTAL_ROWS:,} rows; found {actual_rows:,}.")
        return actual_rows
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_data()
