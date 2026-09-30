from faker import Faker
from datetime import datetime

import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1", #address of database server
    port=3306, #"door" of address to knock on
    user="root", #which database user to log in
    password="labpass", #password for that specific user
    database="schemalab" #which database to connect to
)

fake = Faker()

TOTAL_ROWS = 1_000_000
BATCH_SIZE = 1_000

print("Successfully connected.")

cursor = connection.cursor() #cursor = object used to send SQL commands & get results back through existing connection

insert_query = """
    INSERT INTO user_table
    (first_name, middle_name, last_name, birth_date, email_address, phone_number, country, username, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
"""
# %s is used as a placeholder for each value

for batch_num in range(TOTAL_ROWS // BATCH_SIZE):
    rows = [] #create an empty list
    for i in range(BATCH_SIZE): #loops 10 time
        row = (
            fake.first_name(),
            fake.first_name(),
            fake.last_name(),
            fake.date_of_birth(),
            fake.email(),
            fake.phone_number(),
            fake.country(),
            fake.user_name(),
            datetime.now()
            )
        rows.append(row) #add onto already existing list

    cursor.executemany(insert_query, rows)
    connection.commit()

    print("Inserted batch", batch_num + 1, "-total rows so far:", (batch_num + 1) * BATCH_SIZE)
