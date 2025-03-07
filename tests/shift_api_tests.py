from starlette.testclient import TestClient

def test_should_create_shift(http: TestClient) -> None:
    response = http.post("/shifts")
    assert response.status_code == 201
    assert "id" in response.json()
    assert "status" in response.json()
    assert "open" == response.json()["status"]

def test_should_open_shift(http: TestClient) -> None:
    response = http.post("/shifts")
    assert response.status_code == 201
    shift_id = response.json()["id"]

    response = http.post(f"/shifts/{shift_id}/open")
    assert response.status_code == 200
    assert "open" == response.json()["status"]

def test_should_close_shift(http: TestClient) -> None:
    response = http.post("/shifts")
    assert response.status_code == 201
    shift_id = response.json()["id"]

    response = http.post(f"/shifts/{shift_id}/close")
    assert response.status_code == 200
    assert "close" == response.json()["status"]

def test_should_add_receipt_to_shift(http: TestClient) -> None:
    response = http.post("/shifts")
    assert response.status_code == 201
    shift_id = response.json()["id"]

    response = http.post("/receipts")
    assert response.status_code == 201
    receipt_id = response.json()["id"]

    response = http.post(f"/shifts/{shift_id}/receipts/{receipt_id}")
    assert response.status_code == 200
    assert receipt_id in response.json()["receipts"]