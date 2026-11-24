import asyncio
import tomllib

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from settings import CODEX_CONFIG_PATH, MCP_SERVER_NAME


def test_server_connection() -> None:
    """
    Reads the command you configured for Codex in `config.toml` and prepares it for the test client to start the server.
    The TOML section is named `[mcp_servers.userstory]`. In the Python dictionary, that becomes a `userstory` dictionary
    inside `mcp_servers`.
    `StdioServerParameters` collects the information the test client needs to start the server:
    - `command`: the Python interpreter.
    - `args`: the path to `userstory_server.py`.
    - `cwd`: the working directory.

    `server_config.get("cwd")` is used because `cwd` is optional. If it isn’t present, `.get()` returns `None`.

    check_connection() defines an asynchronous function. Calling it creates a coroutine; it doesn’t run the function
    immediately; asyncio.run(check_connection()) runs that coroutine.

    stdio_client(parameters) starts the server process and gives us a reader and writer for communication.
    ClientSession(reader, writer) uses them to create an MCP session. On leaving the block, the session and
    connection are cleaned up.

    'await' runs the asynchronous initialization operation and waits for the server’s response. Once the response
    arrives, it is assigned to info and tools.
    """
    with CODEX_CONFIG_PATH.open("rb") as config_file:
        config = tomllib.load(config_file)
    server_config = config["mcp_servers"][MCP_SERVER_NAME]
    parameters = StdioServerParameters(
        command=server_config["command"],
        args=server_config["args"],
        cwd=server_config.get("cwd"),
    )

    async def check_connection() -> None:
        async with (
            stdio_client(parameters) as (reader, writer),
            ClientSession(reader, writer) as session,
        ):
            info = await session.initialize()
            # Test assertion
            assert info.server_info.name == "OSplusDB"
            tools = await session.list_tools()
            tool_names = {tool.name for tool in tools.tools}
            # Test assertion
            assert tool_names == {
                "list_customers",
                "list_customers_via_api",
                "insert_customer",
                "insert_customer_via_api",
                "update_customer",
                "update_customer_via_api",
                "delete_customer",
                "delete_customer_via_api",
            }

            result = await session.call_tool("list_customers", {})
            # Test assertion
            assert not result.is_error

    asyncio.run(check_connection())
