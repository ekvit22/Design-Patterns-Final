from unittest.mock import ANY

from starlette.testclient import TestClient


def test_should_create_product(http: TestClient) -> None:
    response = http.post("/products", json={
                                      "unit": "27b4f218-1cc2-4694-b131-ad481dc08901",
                                      "name": "Apple",
                                      "barcode": "1234567890",
                                      "price": 520},)
    assert response.status_code == 201
    assert response.json() == {"id": ANY,
                               "unit": "27b4f218-1cc2-4694-b131-ad481dc08901",
                                      "name": "Apple",
                                      "barcode": "1234567890",
                                      "price": 520}

    cur_id = response.json().get("id")

    response = http.post("/products", json={
        "unit": "27b4f218-1cc2-4694-b131-ad481dc08901",
        "name": "Apple",
        "barcode": "1234567890",
        "price": 520}, )
    assert response.status_code == 409

    response = http.get("/products/"+cur_id)
    assert response.json() == {"id": ANY,
                               "unit": "27b4f218-1cc2-4694-b131-ad481dc08901",
                                      "name": "Apple",
                                      "barcode": "1234567890",
                                      "price": 520}

    response = http.get("/products/")
    assert response.json()[0] == {"id": ANY,
                                  "unit": "27b4f218-1cc2-4694-b131-ad481dc08901",
                                      "name": "Apple",
                                      "barcode": "1234567890",
                                      "price": 520}

    http.patch("/products/"+cur_id,json={"price": 530})
    response = http.get("/products/" + cur_id)
    assert response.json() == {"id": ANY,
                               "unit": "27b4f218-1cc2-4694-b131-ad481dc08901",
                               "name": "Apple",
                               "barcode": "1234567890",
                               "price": 530}

def test_should_get_sales_data(http: TestClient) -> None:
    response = http.post("/receipts", json={})
    receipt_id = response.json().get("id")
    response = http.post("/products", json={
        "unit": "27b4f218-1cc2-4694-b131-ad481dc08902",
        "name": "Apple",
        "barcode": "1234567890",
        "price": 520}, )
    product_id = response.json().get("id")
    response = http.post("/receipts/" + receipt_id + "/products",
                         json={"id": str(product_id), "quantity": 123}, )
    http.patch("/receipts/"+receipt_id, json={"status":"closed"})
    response = http.post("/receipts", json={})
    assert response.status_code == 201
    assert response.json() == {"id": ANY, "status": "open",
                               "products": [],
                               "total": 0}
    receipt_id = response.json().get("id")
    response = http.post("/receipts/" + receipt_id + "/products",
                         json={"id": str(product_id), "quantity": 1},)
    http.patch("/receipts/" + receipt_id, json={"status": "closed"})
    response = http.get("/sales/")
    assert response.status_code == 200
    assert response.json().get("revenue") == 64480