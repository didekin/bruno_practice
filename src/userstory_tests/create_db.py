import sqlite3
from pathlib import Path

# 1. Read the SQL instructions.
sql = Path("sql/customer.sql").read_text()

# 2. Open the database, creating the file if it doesn't exist.
connection = sqlite3.connect("osplus_local.db")

# 3. Run the SQL instructions to create the table.
connection.executescript(sql)

# 4. Close the database connection.
connection.close()
