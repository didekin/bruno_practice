from mcp.server.mcpserver import MCPServer

from userstory_tests import customer_db

mcp = MCPServer("OSplusDB")


@mcp.tool()
def list_customers() -> list[tuple[int, str | None, str | None, str | None]]:
    """List all customers, ordered by customer ID."""
    return customer_db.list_customers()


@mcp.tool()
def insert_customer(name: str, surname: str, email: str) -> int:
    """Insert a customer and return the new customer ID."""
    return customer_db.insert_customer(name, surname, email)


@mcp.tool()
def update_customer(
    customer_id: int,
    name: str,
    surname: str,
    email: str,
) -> bool:
    """Update a customer. Return True if the customer exists."""
    return customer_db.update_customer(customer_id, name, surname, email)


@mcp.tool()
def delete_customer(customer_id: int) -> bool:
    """Delete a customer. Return True if the customer existed."""
    return customer_db.delete_customer(customer_id)


def main() -> None:
    # Wait for MCP requests over standard input and output.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
