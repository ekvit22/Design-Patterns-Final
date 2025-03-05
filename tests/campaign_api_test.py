from unittest.mock import ANY

from starlette.testclient import TestClient


def test_should_create_unit(http: TestClient) -> None:
    response = http.post("/campaigns", json={"name": "test", "description": "testing"},)
    assert response.status_code == 201
    assert response.json() == {"id": ANY, "name": "test", "description": "testing"}

    response = http.delete("/campaigns/" + response.json()["id"])

    assert response.status_code == 201

    response = http.get("/campaigns/")

    assert response.status_code == 201
    assert len(response.json()) == 0

    response = http.post("/campaigns",
                json={"name": "test", "description": "testing"}, )

    response = http.get("/campaigns/")

    assert len(response.json()) == 1



