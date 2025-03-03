from app.core.constants import GEL, USD, EUR, GEL_TO_EUR
from app.services.receipt_service import ReceiptService
import unittest
from unittest.mock import Mock, patch

class ReceiptServiceTests(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock()
        self.receipt_service = ReceiptService(self.mock_repository)

    def test_get_total(self):
        mock_receipt = Mock()
        mock_receipt.total = 100

        result = self.receipt_service.get_total(mock_receipt)
        self.assertEqual(result, 100)

    def test_change_currency(self):
        self.assertAlmostEqual(self.receipt_service.change_currency(100, 2.5), 40.0)
        self.assertAlmostEqual(self.receipt_service.change_currency(250, 2.795), 89.445, places=3)
        self.assertAlmostEqual(self.receipt_service.change_currency(0, 2.918), 0.0)

        expected_value = 10000 / 2.795
        self.assertAlmostEqual(self.receipt_service.change_currency(10000, 2.795), expected_value, places=3)

    def test_calculate_payment_gel(self):
        mock_receipt = Mock()
        mock_receipt.total = 100
        self.receipt_service.repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1234", GEL)
        self.assertEqual(result, 100)
        self.receipt_service.repository.read.assert_called_once_with("1234")

    def test_calculate_payment_usd(self):
        mock_receipt = Mock()
        mock_receipt.total = 279
        self.receipt_service.repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("2222", USD)
        self.assertEqual(result, 99)
        self.receipt_service.repository.read.assert_called_once_with("2222")

    def test_calculate_payment_eur(self):
        mock_receipt = Mock()
        mock_receipt.total = 291
        self.receipt_service.repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1222", EUR)
        self.assertEqual(result, 99)
        self.receipt_service.repository.read.assert_called_once_with("1222")

    def test_calculate_payment_rounding(self):
        mock_receipt = Mock()
        mock_receipt.total = 280
        self.receipt_service.repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1111", USD)
        self.assertEqual(result, 100)

        mock_receipt.total = 142
        result = self.receipt_service.calculate_payment("1111", EUR)
        self.assertEqual(result, 48)

    def test_calculate_payment_edge_cases(self):
        mock_receipt = Mock()
        mock_receipt.total = 0
        self.receipt_service.repository.read.return_value = mock_receipt

        result = self.receipt_service.calculate_payment("1111", USD)
        self.assertEqual(result, 0)

        mock_receipt.total = 1000000
        result = self.receipt_service.calculate_payment("1111", EUR)
        self.assertEqual(result, int(1000000 / GEL_TO_EUR))