# Local database

The project uses a local SQLite database named `osplus_local.db`. Python
includes the `sqlite3` module, so no separate SQLite server or Python package
is required.

## Create the database

From the project root, run:

```bash
uv run python src/userstory_tests/create_db.py
```

The script reads the SQL definition in `sql/customer.sql` and creates the
database and its tables if they do not already exist.

Run the script from the project root: its paths are relative to the current
working directory.

Running the script again does not modify an existing table or delete its rows.

## Database access

The functions in `src/userstory_tests/customer_db.py` provide access to the
customer data. The MCP server uses these functions to respond to requests
from Codex.

The shared database path is defined in `src/settings.py`.

For information about running the project's tests, see [Testing](testing.md).
