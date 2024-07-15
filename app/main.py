from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body

from .models import SalesOrder

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

order_db: List[SalesOrder] = [
    SalesOrder(
        id="c83282f3-1f55-4206-88f1-e0de75565377",
        invoice_number="1",
        date_created="2024-07-12T10:56:44.697700"
    ),
    SalesOrder(
        id="c83282f3-1f55-4206-88f1-e0de75512345",
        invoice_number="2",
        date_created="2024-07-12T10:59:44.697700",
        )
]

@app.get("/")
async def root():
    return {"Greetings Human"}

@app.get("/api/v1/orders/{order_id}")
async def get_order(order_id: UUID):
    for order in order_db:
        if order.id == order_id:
            return order
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"order with id: {order_id} was not found"
        )

@app.get("/api/v1/orders")
async def get_orders():
    return order_db

@app.post("/api/v1/orders", status_code = status.HTTP_201_CREATED)
async def create_order(order: SalesOrder = Body(...)):
    order_db.append(order)
    return {"id": order.id}

@app.delete("/api/v1/orders/{order_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: UUID):
    index = find_order_index(order_id)
    if index is not None:
        order_db.pop(index)
        return
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"order with id: {order_id} was not found"
        )

@app.put("/api/v1/orders/{order_id}")
async def update_order(order_id: UUID, order: SalesOrder):
    index = find_order_index(order_id)
    if index is not None:
        order_dict: SalesOrder = order.model_dump()
        order_dict['id'] = order_id
        print(f"..................... {order.id}")
        print(f"id == {order_dict['id']}")
        order_db[index] = order_dict
        return order_dict
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"order with id: {order_id} was not found"
    )

def find_order_index(order_id):
    for i, o in enumerate(order_db):
        if o['id'] == order_id:
            return i
