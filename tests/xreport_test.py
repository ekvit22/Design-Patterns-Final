import unittest
from unittest.mock import Mock

from app.core.receipt import Products, Receipt
from app.core.shift import Shift
from app.core.xreport import XReport
from app.infra.in_memory import InMemory
from app.services.xreport_service import XReportService


class XReportServiceTests(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock()
        self.mock_shift_repository = Mock()
        self.mock_receipt_repository = Mock()
        self.xreport_service = XReportService(
            self.mock_repository,
            self.mock_shift_repository,
            self.mock_receipt_repository
        )

    def test_generate_x_report_success(self):
        shift_id = "shift-123"
        mock_shift = Mock()
        mock_shift.id = shift_id
        mock_shift.status = "open"
        mock_shift.receipts = ["receipt-1", "receipt-2"]

        expected_report = XReport(
            id="report-123",
            shift_id=shift_id,
            total_receipts=2,
            items_sold={"product-1": 3, "product-2": 1},
            revenue=650.0
        )

        self.mock_shift_repository.read.return_value = mock_shift
        self.mock_repository.generate_x_report.return_value = expected_report

        result = self.xreport_service.generate_x_report(shift_id, None, None)

        self.mock_shift_repository.read.assert_called_once_with(shift_id)
        self.mock_repository.generate_x_report.assert_called_once_with(
            shift_id, mock_shift, self.mock_receipt_repository
        )
        self.assertEqual(result, expected_report)
        self.assertEqual(result.id, expected_report.id)
        self.assertEqual(result.shift_id, shift_id)
        self.assertEqual(result.total_receipts, 2)
        self.assertEqual(result.items_sold, {"product-1": 3, "product-2": 1})
        self.assertEqual(result.revenue, 650.0)

    def test_generate_x_report_nonexistent_shift(self):
        shift_id = "nonexistent-shift"
        self.mock_shift_repository.read.return_value = None

        with self.assertRaises(Exception) as context:
            self.xreport_service.generate_x_report(shift_id, None, None)

        self.assertIn(f"Shift with id<{shift_id}> does not exist", str(context.exception))
        self.mock_shift_repository.read.assert_called_once_with(shift_id)
        self.mock_repository.generate_x_report.assert_not_called()

    def test_generate_x_report_empty_shift(self):
        shift_id = "empty-shift"
        mock_shift = Mock()
        mock_shift.id = shift_id
        mock_shift.receipts = []

        self.mock_shift_repository.read.return_value = mock_shift
        self.mock_repository.generate_x_report.return_value = None

        with self.assertRaises(Exception) as context:
            self.xreport_service.generate_x_report(shift_id, None, None)

        self.assertIn(f"Could not generate X-report for shift<{shift_id}>", str(context.exception))
        self.mock_shift_repository.read.assert_called_once_with(shift_id)
        self.mock_repository.generate_x_report.assert_called_once_with(
            shift_id, mock_shift, self.mock_receipt_repository
        )





def test_generate_x_report_in_memory() -> None:
    in_memory = InMemory()
    xreport_repo = in_memory.xreport()
    shift_repo = in_memory.shifts()
    receipt_repo = in_memory.receipts()

    shift = Shift(id="shift-123", status="open", receipts=["receipt-1", "receipt-2"])
    shift_repo.create(shift)

    receipt1 = Receipt(
        id="receipt-1",
        status="closed",
        products=[
            Products(id="product-1", quantity=2, price=100, total=200),
            Products(id="product-2", quantity=1, price=150, total=150)
        ],
        total=350
    )

    receipt2 = Receipt(
        id="receipt-2",
        status="closed",
        products=[
            Products(id="product-1", quantity=1, price=100, total=100),
            Products(id="product-3", quantity=3, price=75, total=225)
        ],
        total=325
    )

    receipt_repo.create(receipt1)
    receipt_repo.create(receipt2)

    result = xreport_repo.generate_x_report("shift-123", shift, receipt_repo)

    assert result is not None
    assert result.shift_id == "shift-123"
    assert result.total_receipts == 2

    assert result.items_sold["product-1"] == 3
    assert result.items_sold["product-2"] == 1
    assert result.items_sold["product-3"] == 3

    assert result.revenue == 675.0


def test_generate_x_report_empty_shift() -> None:
    in_memory = InMemory()
    xreport_repo = in_memory.xreport()
    shift_repo = in_memory.shifts()
    receipt_repo = in_memory.receipts()

    shift = Shift(id="empty-shift", status="open", receipts=[])
    shift_repo.create(shift)

    result = xreport_repo.generate_x_report("empty-shift", shift, receipt_repo)

    assert result is None


def test_generate_x_report_nonexistent_receipts() -> None:
    in_memory = InMemory()
    xreport_repo = in_memory.xreport()
    shift_repo = in_memory.shifts()
    receipt_repo = in_memory.receipts()

    shift = Shift(id="bad-shift", status="open", receipts=["nonexistent-1", "nonexistent-2"])
    shift_repo.create(shift)

    result = xreport_repo.generate_x_report("bad-shift", shift, receipt_repo)

    assert result is not None
    assert result.total_receipts == 2
    assert result.items_sold == {}
    assert result.revenue == 0.0

