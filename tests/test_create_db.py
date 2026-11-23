import sqlite3

from settings import DATABASE_PATH


def test_customer_table_columns() -> None:
    # Open the database in read-only mode.
    database_uri = f"{DATABASE_PATH.as_uri()}?mode=ro"
    connection = sqlite3.connect(database_uri, uri=True)

    # PRAGMA is a SQLite command for inspecting or changing SQLite-specific settings and information. SQLite returns
    # one row of information for each column. Each row includes the column’s position, name, type and whether it is
    # part of the primary key.
    columns = connection.execute("PRAGMA table_info(CUSTOMER)").fetchall()

    connection.close()

    # Extract the name from each column's information.
    column_names = [column[1] for column in columns]

    assert column_names == [
        "customer_id",
        "name",
        "surname",
        "email",
    ]
