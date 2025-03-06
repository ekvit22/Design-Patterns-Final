import unittest
from typing import Optional
from unittest.mock import Mock, patch

from app.core.constants import EUR, GEL, GEL_TO_EUR, USD
from app.core.product import Product
from app.core.receipt import Products, Receipt
from app.schemas.receipt import AddProductRequest
from app.services.receipt_service import ReceiptService


class ReceiptServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_repository = Mock()
        self.receipt_service = ReceiptService(self.mock_repository)

    def test_get_total(self) -> None:
        mock_receipt = Mock()
        mock_receipt.total = 100

        result = self.receipt_service.get_total(mock_receipt)
        self.assertEqual(result, 100)

    def test_change_currency(self) -> None:
        self.assertAlmostEqual(self.receipt_service.change_currency(100, 2.5),
                               40.0)
        self.assertAlmostEqual(self.receipt_service.change_currency(250, 2.795),
                               round(250 / 2.795, 3), places=3)

    def test_calculate_payment_gel(self) -> None:
        mock_receipt = Mock()
        mock_receipt.total = 100
        self.mock_repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1234", GEL)
        self.assertEqual(result, 100)
        self.mock_repository.read.assert_called_once_with("1234")

    def test_calculate_payment_usd(self) -> None:
        mock_receipt = Mock()
        mock_receipt.total = 279
        self.mock_repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("2222", USD)
        self.assertAlmostEqual(round(result, 2), round(99.82110912343471, 2), places=2)
        self.mock_repository.read.assert_called_once_with("2222")

    def test_calculate_payment_eur(self) -> None:
        mock_receipt = Mock()
        mock_receipt.total = 291
        self.mock_repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1222", EUR)
        self.assertAlmostEqual(round(result, 2), round(99.72583961617546, 2), places=2)
        self.mock_repository.read.assert_called_once_with("1222")

    def test_calculate_payment_rounding(self) -> None:
        mock_receipt = Mock()
        mock_receipt.total = 280
        self.mock_repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1111", USD)
        self.assertAlmostEqual(round(result, 2), round(100.1788908765653, 2), places=2)

        mock_receipt.total = 142
        result = self.receipt_service.calculate_payment("1111", EUR)
        self.assertAlmostEqual(round(result, 2), round(48.66346812885538, 2), places=2)

    def test_calculate_payment_edge_cases(self) -> None:
        mock_receipt = Mock()
        mock_receipt.total = 0
        self.mock_repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1111", USD)
        self.assertEqual(result, 0)

        mock_receipt.total = 1000000
        result = self.receipt_service.calculate_payment("1111", EUR)
        expected = round(1000000 / GEL_TO_EUR, 2)
        self.assertAlmostEqual(result, expected, places=2)

    def test_create(self) -> None:
        expected_receipt = Receipt(id="uuid1", status="open", products=[], total=0)
        self.mock_repository.create.return_value = expected_receipt

        with patch('uuid.uuid4', return_value="uuid1"):
            result = self.receipt_service.create()

        self.assertEqual(result.id, "uuid1")
        self.assertEqual(result.status, "open")
        self.assertEqual(result.products, [])
        self.assertEqual(result.total, 0)

    def test_read_receipt(self) -> None:
        expected_receipt = Receipt(id="receipt-1", status="open",
                                   products=[], total=0)
        self.mock_repository.read.return_value = expected_receipt

        result = self.receipt_service.read("receipt-1")

        self.assertEqual(result, expected_receipt)
        self.mock_repository.read.assert_called_once_with("receipt-1")

    def test_open_receipt(self) -> None:
        mock_receipt = Receipt(id="receipt-1", status="closed", products=[], total=0)
        self.mock_repository.read.return_value = mock_receipt
        self.receipt_service.open_receipt("receipt-1")
        self.mock_repository.open_receipt.assert_called_once_with("receipt-1")
        mock_receipt.status = "open"
        self.mock_repository.read.return_value = mock_receipt
        result = self.receipt_service.read("receipt-1")
        self.assertEqual(result.status, "open")

    def test_close_receipt(self) -> None:
        mock_receipt = Receipt(id="receipt-1", status="open", products=[], total=0)
        self.mock_repository.read.return_value = mock_receipt
        self.receipt_service.close_receipt("receipt-1")
        self.mock_repository.close_receipt.assert_called_once_with("receipt-1")
        mock_receipt.status = "closed"
        self.mock_repository.read.return_value = mock_receipt
        result = self.receipt_service.read("receipt-1")
        self.assertEqual(result.status, "closed")

    def test_add_product_to_receipt(self) -> None:
        existing_product = Products(id="prod-1", quantity=2, price=50, total=100)
        existing_receipt = Receipt(id="receipt-1", status="open",
                                   products=[existing_product], total=100)
        self.mock_repository.read.return_value = existing_receipt

        new_product = Product(id="prod-2", unit_id="2", name="prod2",
                              price=75, barcode="12")
        request = AddProductRequest(id="prod-2", quantity=2)

        result = self.receipt_service.add_product("receipt-1", new_product, request)

        self.assertEqual(len(result.products), 2)
        self.assertEqual(result.products[1].id, "prod-2")
        self.assertEqual(result.products[1].quantity, 2)
        self.assertEqual(result.products[1].price, 75)
        self.assertEqual(result.products[1].total, 150)
        self.assertEqual(result.total, 250)
        self.mock_repository.update.assert_called_once()

    def test_get_every_receipt(self) -> None:
        receipt1 = Receipt(id="receipt-1", status="open", products=[], total=0)
        receipt2 = Receipt(id="receipt-2", status="closed", products=[], total=100)

        def mock_read(receipt_id: str) -> Optional[Receipt]:
            if receipt_id == "receipt-1":
                return receipt1
            elif receipt_id == "receipt-2":
                return receipt2
            return None

        self.mock_repository.read.side_effect = mock_read

        result = self.receipt_service.get_every_receipt(["receipt-1", "receipt-2"])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], receipt1)
        self.assertEqual(result[1], receipt2)
