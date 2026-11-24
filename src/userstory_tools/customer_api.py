from enum import Enum
from typing import Annotated, Any

from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel

from userstory_tools import customer_db

app = FastAPI(title="Customer API")


class CustomerInput(BaseModel):
    name: str
    surname: str
    email: str


class Customer(CustomerInput):
    customer_id: int


class CustomerField(str, Enum):
    NAME = "name"
    SURNAME = "surname"
    EMAIL = "email"


@app.get("/customers")
def list_customers() -> list[Customer]:
    customers = customer_db.list_customers()

    return [
        Customer(
            customer_id=customer_id,
            name=name,
            surname=surname,
            email=email,
        )
        for customer_id, name, surname, email in customers
    ]


@app.post("/customers", status_code=201)
def create_customer(customer: CustomerInput) -> Customer:
    customer_id = customer_db.insert_customer(
        customer.name,
        customer.surname,
        customer.email,
    )
    return Customer(
        customer_id=customer_id,
        **customer.model_dump(),
    )


# If the call succeeds, customer_update_responses is not used to produce the response. It only tells FastAPI how to
# describe the possible 404 response in the OpenAPI documentation.
customer_not_found_responses: dict[int | str, dict[str, Any]] = {
    404: {"description": "Customer not found"},
}


@app.patch(
    "/customers/{customer_id}",
    responses=customer_not_found_responses,
)
def update_customer(
    customer_id: int,
    customer: Annotated[dict[CustomerField, str], Body(min_length=1)],
) -> bool:
    updated = customer_db.update_customer(
        customer_id,
        name=customer.get(CustomerField.NAME),
        surname=customer.get(CustomerField.SURNAME),
        email=customer.get(CustomerField.EMAIL),
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated


@app.delete(
    "/customers/{customer_id}",
    responses=customer_not_found_responses,
)
def delete_customer(customer_id: int) -> bool:
    deleted = customer_db.delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return deleted
