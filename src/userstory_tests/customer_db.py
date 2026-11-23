import sqlite3
from contextlib import closing

from settings import DATABASE_PATH


def insert_customer(name: str, surname: str, email: str) -> int:
    """
    Insert a customer into the local database.
    A SQLite connection can be used with 'with', but its behavior may be surprising: it manages the
    transaction—committing successful changes or rolling them back after an error. It does not close the connection
    when the block ends. closing(...) closes the connection afterwards.
    """
    database_uri = f"{DATABASE_PATH.as_uri()}?mode=rw"

    with (
        closing(sqlite3.connect(database_uri, uri=True)) as connection,
        connection,
    ):
        cursor = connection.execute(
            """
            INSERT INTO CUSTOMER (name, surname, email)
            VALUES (?, ?, ?)
            """,
            (name, surname, email),
        )
        customer_id = cursor.lastrowid

    assert customer_id is not None
    return customer_id


def update_customer(
    customer_id: int,
    name: str,
    surname: str,
    email: str,
) -> bool:
    """Update a customer. Return True if the customer exists."""
    database_uri = f"{DATABASE_PATH.as_uri()}?mode=rw"

    with (
        closing(sqlite3.connect(database_uri, uri=True)) as connection,
        connection,
    ):
        cursor = connection.execute(
            """
            UPDATE CUSTOMER
            SET name    = ?,
                surname = ?,
                email   = ?
            WHERE customer_id = ?
            """,
            (name, surname, email, customer_id),
        )

    return cursor.rowcount > 0


def delete_customer(customer_id: int) -> bool:
    """Delete a customer. Return True if the customer existed."""
    database_uri = f"{DATABASE_PATH.as_uri()}?mode=rw"

    with (
        closing(sqlite3.connect(database_uri, uri=True)) as connection,
        connection,
    ):
        cursor = connection.execute(
            "DELETE FROM CUSTOMER WHERE customer_id = ?",
            (customer_id,),
        )

    return cursor.rowcount > 0


def list_customers() -> list[tuple[int, str | None, str | None, str | None]]:
    """Return all customers, ordered by customer ID."""
    database_uri = f"{DATABASE_PATH.as_uri()}?mode=ro"

    with closing(sqlite3.connect(database_uri, uri=True)) as connection:
        customers = connection.execute(
            """
            SELECT customer_id, name, surname, email
            FROM CUSTOMER
            ORDER BY customer_id
            """
        ).fetchall()

    return customers
