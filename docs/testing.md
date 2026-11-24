# Testing

The project uses pytest. The tests cover the database, customer API, MCP
server, and MCP client connection.

## Prerequisites

Install the project dependencies from the project root:

```bash
uv sync
```

Create the local database before running the tests. See
[Local database](database.md) for setup instructions. The MCP client
connection test also requires the server to be configured in Codex; see
[MCP server](mcp-server.md).

## Start the customer API

The API must be running for the MCP API-tool tests and for manual testing
through Codex. From the project root, start it with:

```bash
uv run uvicorn userstory_tools.customer_api:app
```

Keep Uvicorn running in one terminal while you test in another terminal or
in the Codex app. Stop it with **Ctrl+C** when you have finished.

## Test data

The automated tests use the real local database. Tests that need a customer
create their own test record and remove it during cleanup, including when an
assertion fails. This aims to leave the database as it was before the test.

## Database

`test_create_db.py` checks the table structure, and `test_customer_db.py`
checks the customer database operations.

```bash
uv run pytest tests/test_create_db.py tests/test_customer_db.py
```

## Customer API

`test_customer_api.py` checks the API's GET, POST, PATCH, and DELETE
operations. The tests use FastAPI's `TestClient` to call the application
without starting Uvicorn.

```bash
uv run pytest tests/test_customer_api.py
```

## MCP server

`test_userstory_server.py` checks the registered tools and server functions.
Its API tool tests send HTTP requests to the running FastAPI service.

```bash
uv run pytest tests/test_userstory_server.py
```

## MCP client connection

`test_userstory_client.py` starts the MCP server using the saved Codex
configuration, connects over stdio, and calls a tool. It reads the
configuration path and server name from `src/settings.py`.

```bash
uv run pytest tests/test_userstory_client.py
```

This test uses a Python MCP client; it does not check whether the Codex app
has loaded the server.

## Manual API testing

With Uvicorn running, open the interactive API documentation at
`http://127.0.0.1:8000/docs` to inspect and try the endpoints.

You can create customers for manual tests in either of these ways:

- Call `insert_customer()` from `customer_db.py`.
- Use the POST endpoint in the interactive API documentation. The endpoint
  is implemented in `customer_api.py`.

Keep the customer IDs returned when you create the records; you can use them
to test the PATCH and DELETE endpoints.

**Manual tests do not automatically clean up their data.** Customers created
or changed during manual testing may remain in the database. Delete any test
records you no longer need.

## Manual test with Codex

1. Start the customer API as described above.
2. Open a local conversation in the Codex app. If you have just added or
   changed the MCP server configuration, restart Codex and start a new
   conversation.
3. Use `/mcp` to check that the `userstory` server is connected.
4. Ask Codex:

   > Use the `list_customers_via_api` MCP tool to list the customers.
   > Please confirm which tool you used.

5. Check that Codex used the requested tool and returned the customer list,
   or an empty list if there are no customers.

## Run all tests

With the FastAPI service running, run the full suite from the project root:

```bash
uv run pytest
```
