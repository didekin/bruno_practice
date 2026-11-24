from userstory_tools import customer_db

TEST_CUSTOMER = ("Ada", "Lovelace", "ada@example.com")


def test_insert_customer() -> None:
    customer_id = customer_db.insert_customer(*TEST_CUSTOMER)

    try:
        customers = customer_db.list_customers()

        assert any(customer[0] == customer_id for customer in customers)

    finally:
        customer_db.delete_customer(customer_id)


def test_list_customers() -> None:
    customer_id = customer_db.insert_customer(*TEST_CUSTOMER)

    try:
        customers = customer_db.list_customers()

        assert any(customer[0] == customer_id for customer in customers)

    finally:
        customer_db.delete_customer(customer_id)


def test_update_customer() -> None:
    customer_id = customer_db.insert_customer(*TEST_CUSTOMER)

    try:
        updated = customer_db.update_customer(
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
    customer_id = customer_db.insert_customer(*TEST_CUSTOMER)
    deleted = False

    try:
        deleted = customer_db.delete_customer(customer_id)
        customers = customer_db.list_customers()

        assert deleted
        assert not any(customer[0] == customer_id for customer in customers)

    finally:
        if not deleted:
            customer_db.delete_customer(customer_id)
