# Testing

The project uses pytest. The tests are organized into three groups: database,
MCP server, and MCP client connection.

## Test data

Tests that need a customer create their own test record and remove it during
cleanup, including when an assertion fails. This keeps the tests independent
of existing customer data and aims to leave the database as it was before
the test.

## Database

`test_create_db.py` checks the table structure, and `test_customer_db.py`
checks the customer database operations.

Create the local database before running these tests. See
[Local database](database.md) for setup instructions.

To run the database tests from the project root:

```bash
uv run pytest tests/test_create_db.py tests/test_customer_db.py
```

## MCP server

`test_userstory_server.py` checks the registered tools and the server
functions. The tests of the server functions use the local database.

To run the server tests from the project root:

```bash
uv run pytest tests/test_userstory_server.py
```

## MCP client connection

`test_userstory_client.py` starts the server using the saved Codex
configuration, connects to it over stdio, and calls a tool.

The test requires the server to be configured in Codex. It reads the
configuration path and server name from `src/settings.py`. See
[MCP server](mcp-server.md) for setup instructions.

To run the connection test from the project root:

```bash
uv run pytest tests/test_userstory_client.py
```

The test uses a Python MCP client; it does not check whether the Codex app
has loaded the server.

## Run all tests

To run the full suite from the project root:

```bash
uv run pytest
```
