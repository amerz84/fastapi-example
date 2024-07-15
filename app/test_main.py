from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ["Greetings Human"]

def test_get_order():
    response = client.get("/api/v1/orders/c83282f3-1f55-4206-88f1-e0de75565377")
    assert response.status_code == 200
    assert response.json() == {
        "id":"c83282f3-1f55-4206-88f1-e0de75565377",
        "invoice_number":"1",
        "date_created":"2024-07-12T10:56:44.697700"
    }

def test_get_nonexistent_order():
    response = client.get("/api/v1/orders/c83282f3-0000-0000-0000-000075565377")
    assert response.status_code == 404

def test_get_orders():
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_create_order():
    response = client.post("/api/v1/orders", json={
        "invoice_number":"3"
    })
    assert response.status_code == 201
    
def test_delete_order():
    response = client.delete("/api/v1/orders/c83282f3-1f55-4206-88f1-e0de75565377")
    assert response.status_code == 204

def test_update_order():
    order_id = "c83282f3-1f55-4206-88f1-e0de75512345"
    new_data = {
        "id" : order_id,
        "invoice_number":"5",
        "date_created": "2024-07-12T10:00:00.000001"}
    response = client.put(
        url=f"/api/v1/orders/{order_id}", 
        json=new_data
    )
    assert response.json() == {
        "id": order_id,
        **new_data
    }

def test_update_nonexistent_order():
    order_id = "c83282f3-0000-0000-0000-000075565377"
    new_data = {
        "invoice_number":"fake_inv",
        "date_created": "2024-07-12T10:00:00.000001"}
    response = client.put(
        url=f"/api/v1/orders/{order_id}", 
        json=new_data
    )
    assert response.status_code == 404

def test_delete_nonexistent_order():
    response = client.delete("/api/v1/orders/c83282f3-0000-0000-0000-000075565377")
    assert response.status_code == 404