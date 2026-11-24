from fastapi.testclient import TestClient

from userstory_tools import customer_db
from userstory_tools.customer_api import app


def test_list_customers() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )
    try:
        with TestClient(app) as client:
            response = client.get("/customers")

        assert response.status_code == 200
        assert {
            "customer_id": customer_id,
            "name": "Ada",
            "surname": "Lovelace",
            "email": "ada@example.com",
        } in response.json()

    finally:
        customer_db.delete_customer(customer_id)


def test_create_customer() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/customers",
            json={
                "name": "Ada",
                "surname": "Lovelace",
                "email": "ada@example.com",
            },
        )

    customer_id = response.json()["customer_id"]

    try:
        assert response.status_code == 201
        assert response.json() == {
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


def test_update_customer() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )

    try:
        with TestClient(app) as client:
            response = client.patch(
                f"/customers/{customer_id}",
                json={"email": "ada.new@example.com"},
            )

        assert response.status_code == 200
        assert response.json() is True
        assert (
            customer_id,
            "Ada",
            "Lovelace",
            "ada.new@example.com",
        ) in customer_db.list_customers()

    finally:
        customer_db.delete_customer(customer_id)


def test_delete_customer() -> None:
    customer_id = customer_db.insert_customer(
        "Ada", "Lovelace", "ada@example.com"
    )

    try:
        with TestClient(app) as client:
            response = client.delete(f"/customers/{customer_id}")

        assert response.status_code == 200
        assert response.json() is True
        assert not any(
            customer[0] == customer_id
            for customer in customer_db.list_customers()
        )

    finally:
        customer_db.delete_customer(customer_id)
