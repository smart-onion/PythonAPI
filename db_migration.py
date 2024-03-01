import dotenv
import os

import psycopg2
import pyodbc

dotenv.load_dotenv()

MDB = r'D:\Mano\pythonAPI\API\DsiBilling.mdb'
DRV = '{Microsoft Access Driver (*.mdb)}'
PWD = 'pw'

conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + MDB
db_params = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'port': os.environ.get('DB_PORT')
}

# Establish a connection
conn = pyodbc.connect(conn_str)
pg_conn = psycopg2.connect(**db_params)

# Create a cursor from the connection
cursor = conn.cursor()
pg_cursor = pg_conn.cursor()

# Example query
query = "SELECT USER_NAME, IDNUM, FIRST_NAME, LAST_NAME FROM dbul"
pg_query = "INSERT INTO guests (guest, folio_id, f_name, l_name) VALUES (%s, %s, %s, %s)"

# Execute the query
cursor.execute(query)
# Fetch all the rows
rows = cursor.fetchall()

# Print the results
for row in rows:

    pg_cursor.execute(pg_query, (row[0], row[1], row[2], row[3]))

pg_conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
pg_cursor.close()
pg_conn.close()