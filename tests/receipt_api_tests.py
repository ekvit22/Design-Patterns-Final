# import unittest
#
# from starlette.testclient import TestClient
#
# class ReceiptApiTests(unittest.TestCase):
#     def test_read_receipt(http: TestClient) -> None:
#         test_receipt = {
#             "id": "1234",
#             "status": "open",
#             "products": [
#                 {
#                     "id": "101",
#                     "quantity": 2,
#                     "price": 25,
#                     "total": 50
#                 },
#                 {
#                     "id": "102",
#                     "quantity": 1,
#                     "price": 50,
#                     "total": 50
#                 }
#             ],
#             "total": 100
#         }
#
#         response = http.post("/receipts", json=test_receipt)
#         assert response.status_code == 201
#
#         response = http.get("/receipts?rec_id=1234")
#         assert response.status_code == 200
#         assert response.json() == test_receipt
#
#         response = http.delete("/receipts/1234")
#         assert response.status_code == 200
#
#     def test_get_discounted_price(http: TestClient) -> None:
#         test_receipt = {
#             "id": "1234",
#             "status": "open",
#             "products": [
#                 {
#                     "id": "201",
#                     "quantity": 2,
#                     "price": 50,
#                     "total": 100
#                 }
#             ],
#             "total": 100
#         }
#
#         test_campaign = {
#             "name": "discount_test",
#             "description": "discount;201;50"
#         }
#
#         response = http.post("/receipts", json=test_receipt)
#         assert response.status_code == 201
#
#         response = http.post("/campaigns", json=test_campaign)
#         assert response.status_code == 201
#
#         response = http.get("/receipts/1234/discounted_price")
#         assert response.status_code == 200
#         assert response.json() == 50
#
#         response = http.delete("/receipts/1234")
#         response = http.delete("/campaigns/" + test_campaign["id"])
#         assert response.status_code == 200
#
#     def test_calculate_payment(http: TestClient) -> None:
#         test_receipt = {
#             "id": "1234",
#             "status": "open",
#             "products": [
#                 {
#                     "id": "301",
#                     "quantity": 3,
#                     "price": 50,
#                     "total": 150
#                 },
#                 {
#                     "id": "302",
#                     "quantity": 1,
#                     "price": 129,
#                     "total": 129
#                 }
#             ],
#             "total": 279
#         }
#
#         response = http.post("/receipts", json=test_receipt)
#         assert response.status_code == 201
#
#         response = http.post("/receipts/1234/quotes?currency=GEL")
#         assert response.status_code == 200
#         assert response.json() == 279
#
#         response = http.post("/receipts/1234/quotes?currency=USD")
#         assert response.status_code == 200
#         assert response.json() == 99
#
#         response = http.post("/receipts/1003/quotes?currency=EUR")
#         assert response.status_code == 200
#         assert response.json() == 95
#
#         response = http.delete("/receipts/1003")
#         assert response.status_code == 200
#
#     def test_complete_payment(http: TestClient) -> None:
#         test_receipt = {
#             "id": "1234",
#             "status": "open",
#             "products": [
#                 {
#                     "id": "401",
#                     "quantity": 1,
#                     "price": 200,
#                     "total": 200
#                 }
#             ],
#             "total": 200
#         }
#
#         response = http.post("/receipts", json=test_receipt)
#         assert response.status_code == 201
#
#         response = http.get("/receipts?rec_id=1234")
#         assert response.status_code == 200
#         assert response.json()["status"] == "open"
#
#         response = http.post("/receipts/1234/payments")
#         assert response.status_code == 200
#
#         response = http.get("/receipts?rec_id=1234")
#         assert response.status_code == 200
#         assert response.json()["status"] == "closed"
#
#         response = http.delete("/receipts/1234")
#         assert response.status_code == 200