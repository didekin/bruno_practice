# MCP server

The MCP server allows Codex to access the customer database through the
functions in `customer_db.py`.

```text
Codex, acting as the MCP client
    ↕ MCP requests and responses over stdio
userstory_server.py
    ↕
customer_db.py
    ↕
osplus_local.db
```

The server is defined in `src/mcp_integration/userstory_server.py`. It exposes
the customer database operations as MCP tools. Codex acts as the MCP client:
it discovers the available tools and can request their execution.

The server and client communicate through standard input and output
(`stdio`). The server starts when Codex launches it using the configured
command.

## Connect the server to Codex

Add an entry for the server to `~/.codex/config.toml`, preserving any existing
contents. Replace `/path/to/userstory_tests` with the absolute path to your
project:

```toml
[mcp_servers.userstory]
command = "/path/to/userstory_tests/.venv/bin/python"
args = ["/path/to/userstory_tests/src/mcp_integration/userstory_server.py"]
cwd = "/path/to/userstory_tests"
```

The project environment and local database must already exist. See
[Local database](database.md) for database setup.

After saving the configuration, restart Codex and start a new local
conversation. Use `/mcp` to check that the server is connected. You can then
ask Codex to use the `list_customers` tool from the `userstory` MCP server.

## Tests

For information about testing the server, see [Testing](testing.md).
