import asyncio

from mcp_integration import userstory_server
from userstory_tools import customer_db


def test_customer_tools_are_registered() -> None:
    tools = asyncio.run(userstory_server.mcp.list_tools())
    tool_names = {tool.name for tool in tools}
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


def test_list_customers() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        customers = userstory_server.list_customers()
        assert (
            customer_id,
            "Ada",
            "Lovelace",
            "ada@example.com",
        ) in customers
    finally:
        customer_db.delete_customer(customer_id)


def test_insert_customer() -> None:
    customer_id = userstory_server.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        customers = customer_db.list_customers()
        assert (
            customer_id,
            "Ada",
            "Lovelace",
            "ada@example.com",
        ) in customers
    finally:
        customer_db.delete_customer(customer_id)


def test_update_customer() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        updated = userstory_server.update_customer(
            customer_id, "Grace", "Hopper", "grace@example.com"
        )
        customers = customer_db.list_customers()
        assert updated
        assert (
            customer_id,
            "Grace",
            "Hopper",
            "grace@example.com",
        ) in customers
    finally:
        customer_db.delete_customer(customer_id)


def test_delete_customer() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        deleted = userstory_server.delete_customer(customer_id)
        customers = customer_db.list_customers()
        assert deleted
        assert not any(customer[0] == customer_id for customer in customers)
    finally:
        customer_db.delete_customer(customer_id)


def test_list_customers_via_api() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        customers = userstory_server.list_customers_via_api()
        assert {
            "customer_id": customer_id,
            "name": "Ada",
            "surname": "Lovelace",
            "email": "ada@example.com",
        } in customers
    finally:
        customer_db.delete_customer(customer_id)


def test_insert_customer_via_api() -> None:
    customer = userstory_server.insert_customer_via_api(
        "Ada", "Lovelace", "ada@example.com"
    )
    customer_id = customer["customer_id"]
    assert isinstance(customer_id, int)

    try:
        assert customer == {
            "customer_id": customer_id,
            "name": "Ada",
            "surname": "Lovelace",
            "email": "ada@example.com",
        }
        assert (
            customer_id,
            "Ada",
            "Lovelace",
            "ada@example.com",
        ) in customer_db.list_customers()

    finally:
        customer_db.delete_customer(customer_id)


def test_update_customer_via_api() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        updated = userstory_server.update_customer_via_api(
            customer_id, email="ada.new@example.com"
        )
        assert updated
        assert (
            customer_id,
            "Ada",
            "Lovelace",
            "ada.new@example.com",
        ) in customer_db.list_customers()
    finally:
        customer_db.delete_customer(customer_id)


def test_delete_customer_via_api() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        deleted = userstory_server.delete_customer_via_api(customer_id)
        assert deleted
        assert not any(
            customer[0] == customer_id
            for customer in customer_db.list_customers()
        )
    finally:
        customer_db.delete_customer(customer_id)
