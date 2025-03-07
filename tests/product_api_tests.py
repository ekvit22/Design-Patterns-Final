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
