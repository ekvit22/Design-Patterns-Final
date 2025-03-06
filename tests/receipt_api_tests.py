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

# def test_should_add_product_to_receipt(http: TestClient) -> None:
#     # shevqmna recepti
#     response = http.post("/receipts")
#     assert response.status_code == 201
#     receipt_id = response.json()["id"]
#     assert "id" in response.json()
#
#     # shevqmna producti
#     response = http.post("/products")
#     assert response.status_code == 201
#
#     # chavamato producti recepshi
#     add_product_request = {"id": "prod-1", "quantity": 2}
#     response = http.post(f"/receipts/{receipt_id}/products", json=add_product_request)
#
#     # shevamowmo
#     assert response.status_code == 200
#     assert any(product["id"] == "prod-1" for product in response.json()["products"])

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


# def test_should_get_z_reports(http: TestClient) -> None:
#     # shift shevqmeni
#     response = http.post("/shifts")
#     assert response.status_code == 201
#     shift_id = response.json()["id"]
#
#     # 1 receipt shevqmeni
#     response = http.post("/receipts")
#     assert response.status_code == 201
#     receipt_id1 = response.json()["id"]
#
#     # chavagde receipt1 shiftshi
#     response = http.post(f"/shifts/{shift_id}/receipts/{receipt_id1}")
#     assert response.status_code == 200
#
#     # meore receipt shevmqeni
#     response = http.post("/receipts")
#     assert response.status_code == 201
#     receipt_id2 = response.json()["id"]
#
#     # chavagde meore recepti shiftshi
#     response = http.post(f"/shifts/{shift_id}/receipts/{receipt_id2}")
#     assert response.status_code == 200
#
#     # amoviogo Z reports
#     response = http.get(f"/receipts/{shift_id}/z_reports")
#     assert response.status_code == 200
#     assert len(response.json()) == 2
