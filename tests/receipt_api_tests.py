from unittest.mock import ANY
from starlette.testclient import TestClient

def test_should_read_receipt(http: TestClient) -> None:
    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]

    response = http.get(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    assert response.json()["id"] == receipt_id
    assert "status" in response.json()
    assert "products" in response.json()
    assert "total" in response.json()

def test_should_get_discounted_price(http: TestClient) -> None:
    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]

    response = http.get(f"/receipts/{receipt_id}/discounted_price")
    assert response.status_code == 200
    assert isinstance(response.json(), float)

def test_should_calculate_payment(http: TestClient) -> None:
    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]

    response = http.post(f"/receipts/{receipt_id}/quotes?currency=USD")
    assert response.status_code == 200
    assert isinstance(response.json(), float)

def test_should_complete_payment(http: TestClient) -> None:
    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]

    response = http.post(f"/receipts/{receipt_id}/payments")
    assert response.status_code == 200
