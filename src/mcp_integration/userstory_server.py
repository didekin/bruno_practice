import httpx
from mcp.server.mcpserver import MCPServer

from settings import CUSTOMER_API_URL
from userstory_tools import customer_db

mcp = MCPServer("OSplusDB")


@mcp.tool()
def list_customers() -> list[tuple[int, str, str, str]]:
    """List all customers, ordered by customer ID."""
    return customer_db.list_customers()


@mcp.tool()
def list_customers_via_api() -> list[dict[str, int | str]]:
    """List customers through the customer API."""
    response = httpx.get(f"{CUSTOMER_API_URL}/customers", timeout=10.0)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def insert_customer(name: str, surname: str, email: str) -> int:
    """Insert a customer and return the new customer ID."""
    return customer_db.insert_customer(name, surname, email)


@mcp.tool()
def insert_customer_via_api(
    name: str,
    surname: str,
    email: str,
) -> dict[str, int | str]:
    """Insert a customer through the customer API."""
    response = httpx.post(
        f"{CUSTOMER_API_URL}/customers",
        json={
            "name": name,
            "surname": surname,
            "email": email,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()


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
def update_customer_via_api(
    customer_id: int,
    name: str | None = None,
    surname: str | None = None,
    email: str | None = None,
) -> bool:
    """Update the supplied customer fields through the customer API."""
    fields = {"name": name, "surname": surname, "email": email}
    customer = {
        field: value for field, value in fields.items() if value is not None
    }

    response = httpx.patch(
        f"{CUSTOMER_API_URL}/customers/{customer_id}",
        json=customer,
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()


@mcp.tool()
def delete_customer(customer_id: int) -> bool:
    """Delete a customer. Return True if the customer existed."""
    return customer_db.delete_customer(customer_id)


@mcp.tool()
def delete_customer_via_api(customer_id: int) -> bool:
    """Delete a customer through the customer API."""
    response = httpx.delete(
        f"{CUSTOMER_API_URL}/customers/{customer_id}",
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    # Wait for MCP requests over standard input and output.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
