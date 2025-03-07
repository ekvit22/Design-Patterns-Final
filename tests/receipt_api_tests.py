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

def test_should_create_receipt(http: TestClient) -> None:
    response = http.post("/receipts")
    assert response.status_code == 201
    assert "id" in response.json()
    assert "status" in response.json()
    assert "products" in response.json()
    assert "total" in response.json()

def test_should_add_product_to_receipt(http: TestClient) -> None:
    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]
    assert "id" in response.json()

    response = http.post("/products", json={
                                      "unit": "27b4f218-1cc2-4694-b131-ad481dc08901",
                                      "name": "Apple",
                                      "barcode": "1234567890",
                                      "price": 520})
    assert response.status_code == 201
    id = response.json()["id"]
    add_product_request = {"id": id, "quantity": 2}
    response = http.post(f"/receipts/{receipt_id}/products", json=add_product_request)

    assert response.status_code == 200
    assert len(response.json()["products"]) == 1

def test_should_update_receipt_status(http: TestClient) -> None:
    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]
    request_data = {"status": "closed"}
    response = http.patch(f"/receipts/{receipt_id}", json=request_data)
    assert response.status_code == 200

    request_data = {"status": "open"}
    response = http.patch(f"/receipts/{receipt_id}", json=request_data)
    assert response.status_code == 200


def test_should_get_z_reports(http: TestClient) -> None:
    response = http.post("/shifts")
    assert response.status_code == 201
    id = response.json()["id"]

    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]

    response = http.post(f"/shifts/{id}/receipts/{receipt_id}")
    assert response.status_code == 200

    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]

    response = http.post(f"/shifts/{id}/receipts/{receipt_id}")
    assert response.status_code == 200

    response = http.get(f"/receipts/{id}/z_reports")
    assert response.status_code == 200
    assert len(response.json()) == 2
