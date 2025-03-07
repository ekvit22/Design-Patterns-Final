import unittest
from unittest.mock import Mock

from app.core.shift import Shift
from app.services.shift_service import ShiftService


class ShiftServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_repository = Mock()
        self.shift_service = ShiftService(self.mock_repository)

    def test_create_shift(self) -> None:
        expected_shift = Shift(id="shift-1", status="open", receipts=[])
        self.mock_repository.create_shift.return_value = expected_shift
        result = self.shift_service.create()
        self.assertEqual(result.status, "open")
        self.assertEqual(result.receipts, [])


    def test_open_shift(self) -> None:
        mock_shift = Shift(id="shift-1", status="close", receipts=[])
        self.mock_repository.read.return_value = mock_shift
        self.shift_service.open_shift("shift-1")
        self.mock_repository.open_shift.assert_called_once()
        mock_shift.status = "open"
        self.mock_repository.read.return_value = mock_shift
        result = self.shift_service.read_shift("shift-1")
        if result is None:
            raise AssertionError()
        self.assertEqual(result.status, "open")

    def test_close_shift(self) -> None:
        mock_shift = Shift(id="shift-1", status="open", receipts=[])
        self.mock_repository.read.return_value = mock_shift
        self.shift_service.close_shift("shift-1")
        self.mock_repository.close_shift.assert_called_once()
        mock_shift.status = "close"
        self.mock_repository.read.return_value = mock_shift
        result = self.shift_service.read_shift("shift-1")
        if result is None:
            raise AssertionError()
        self.assertEqual(result.status, "close")

    def test_add_receipt_to_shift(self) -> None:
        self.mock_repository.read.return_value = Shift(id="shift-1",
                                                       status="open", receipts=[])
        self.shift_service.add_receipt_to_shift("shift-1", "receipt-1")
        self.mock_repository.add_receipt_to_shift.assert_called_once_with("shift-1",
                                                                          "receipt-1")

        self.mock_repository.read.return_value.receipts.append("receipt-1")
        shift = self.shift_service.read_shift("shift-1")
        if shift is None:
            raise AssertionError()
        assert "receipt-1" in shift.receipts
        assert len(shift.receipts) == 1

    def test_get_shift_receipt_ids(self) -> None:
        self.mock_repository.get_shift_receipt_ids.return_value = ["receipt-1",
                                                                   "receipt-2"]
        receipt_ids = self.shift_service.get_shift_receipt_ids("shift-1")
        assert receipt_ids == ["receipt-1", "receipt-2"]
        self.mock_repository.get_shift_receipt_ids.assert_called_once_with("shift-1")
        assert len(receipt_ids) == 2


    def test_read_shift(self) -> None:
        self.mock_repository.read.return_value = Shift(id="shift-1",
                                                       status="open",
                                                       receipts=["receipt-1",
                                                                 "receipt-2"])
        shift = self.shift_service.read_shift("shift-1")
        if shift is None:
            raise AssertionError()
        assert shift.id == "shift-1"
        assert shift.status == "open"
        assert shift.receipts == ["receipt-1", "receipt-2"]
        self.mock_repository.read.assert_called_once_with("shift-1")