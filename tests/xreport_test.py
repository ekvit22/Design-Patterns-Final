from typing import Dict, List, Optional
from uuid import uuid4

from app.core.receipt import Products, Receipt
from app.core.repository import Repository
from app.core.shift import Shift
from app.core.xreport import XReport
from app.schemas.sales import SalesData
from app.services.xreport_service import XReportService


def test_xreport_in_memory() -> None:

    class MockXReportRepository(Repository[XReport]):
        def __init__(self, items: Optional[Dict[str, XReport]] = None) -> None:
            self.items = items or {}

        def create(self, item: XReport) -> XReport:
            self.items[item.id] = item
            return item

        def read(self, item_id: str) -> Optional[XReport]:
            return self.items.get(item_id)

        def update(self, item: XReport) -> None:
            self.items[item.id] = item

        def delete(self, item_id: str) -> None:
            if item_id in self.items:
                del self.items[item_id]

        def get_all(self) -> List[XReport]:
            return list(self.items.values())

        def read_with_name(self, item_name: str) -> Optional[XReport]:
            return None

        def read_with_barcode(self, item_barcode: str) -> Optional[XReport]:
            return None

        def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
            pass

        def close_receipt(self, receipt_id: str) -> None:
            pass

        def open_receipt(self, receipt_id: str) -> None:
            pass

        def close_shift(self, shift_id: str) -> None:
            pass

        def open_shift(self, shift_id: str) -> None:
            pass

        def get_every_receipt(self, receipt_ids: List[str]) -> List[XReport]:
            return [self.items[rid] for rid in receipt_ids if rid in self.items]

        def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
            return []

        def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
            return []

        def get_sales_data(self) -> Optional[SalesData]:
            return None

    class MockShiftRepository(Repository[Shift]):
        def __init__(self, items: Optional[Dict[str, Shift]] = None) -> None:
            self.items = items or {}

        def create(self, item: Shift) -> Shift:
            self.items[item.id] = item
            return item

        def read(self, item_id: str) -> Optional[Shift]:
            return self.items.get(item_id)

        def update(self, item: Shift) -> None:
            self.items[item.id] = item

        def delete(self, item_id: str) -> None:
            if item_id in self.items:
                del self.items[item_id]

        def get_all(self) -> List[Shift]:
            return list(self.items.values())

        def read_with_name(self, item_name: str) -> Optional[Shift]:
            return None

        def read_with_barcode(self, item_barcode: str) -> Optional[Shift]:
            return None

        def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
            shift = self.items.get(shift_id)
            if shift:
                shift.receipts.append(receipt_id)

        def close_receipt(self, receipt_id: str) -> None:
            pass

        def open_receipt(self, receipt_id: str) -> None:
            pass

        def close_shift(self, shift_id: str) -> None:
            shift = self.items.get(shift_id)
            if shift:
                shift.status = "close"

        def open_shift(self, shift_id: str) -> None:
            shift = self.items.get(shift_id)
            if shift:
                shift.status = "open"

        def get_every_receipt(self, receipt_ids: List[str]) -> List[Shift]:
            return [self.items[rid] for rid in receipt_ids if rid in self.items]

        def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
            shift = self.items.get(shift_id)
            return shift.receipts if shift else []

        def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
            return []

        def get_sales_data(self) -> Optional[SalesData]:
            return None

    class MockReceiptRepository(Repository[Receipt]):
        def __init__(self, items: Optional[Dict[str, Receipt]] = None) -> None:
            self.items = items or {}

        def create(self, item: Receipt) -> Receipt:
            self.items[item.id] = item
            return item

        def read(self, item_id: str) -> Optional[Receipt]:
            return self.items.get(item_id)

        def update(self, item: Receipt) -> None:
            self.items[item.id] = item

        def delete(self, item_id: str) -> None:
            if item_id in self.items:
                del self.items[item_id]

        def get_all(self) -> List[Receipt]:
            return list(self.items.values())

        def read_with_name(self, item_name: str) -> Optional[Receipt]:
            return None

        def read_with_barcode(self, item_barcode: str) -> Optional[Receipt]:
            return None

        def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
            pass

        def close_receipt(self, receipt_id: str) -> None:
            receipt = self.items.get(receipt_id)
            if receipt:
                receipt.status = "close"

        def open_receipt(self, receipt_id: str) -> None:
            receipt = self.items.get(receipt_id)
            if receipt:
                receipt.status = "open"

        def close_shift(self, shift_id: str) -> None:
            pass

        def open_shift(self, shift_id: str) -> None:
            pass

        def get_every_receipt(self, receipt_ids: List[str]) -> List[Receipt]:
            return [self.items[rid] for rid in receipt_ids if rid in self.items]

        def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
            return []

        def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
            receipt = self.items.get(receipt_id)
            return receipt.products if receipt else []

        def get_sales_data(self) -> Optional[SalesData]:
            return None

    shift_id = str(uuid4())
    shift = Shift(id=shift_id, status="open", receipts=[])

    receipt1_id = str(uuid4())
    receipt1 = Receipt(
        id=receipt1_id,
        status="close",
        products=[
            Products(id="apple", quantity=3, price=1.50, total=4.50),
            Products(id="banana", quantity=2, price=0.75, total=1.50)
        ],
        total=6.00
    )

    receipt2_id = str(uuid4())
    receipt2 = Receipt(
        id=receipt2_id,
        status="close",
        products=[
            Products(id="apple", quantity=1, price=1.50, total=1.50),
            Products(id="orange", quantity=4, price=1.25, total=5.00)
        ],
        total=6.50
    )

    shift.receipts = [receipt1_id, receipt2_id]

    mock_shift_repo = MockShiftRepository({shift_id: shift})
    mock_receipt_repo = MockReceiptRepository({receipt1_id: receipt1,
                                               receipt2_id: receipt2})
    mock_xreport_repo = MockXReportRepository()

    xreport_service = XReportService(mock_xreport_repo,
                                     mock_shift_repo, mock_receipt_repo)

    receipts: List[Receipt | None] = [receipt1, receipt2]

    xreport = xreport_service.generate_x_report(shift_id, receipts)

    assert xreport.shift_id == shift_id
    assert xreport.total_receipts == 2
    assert xreport.revenue == 12.50
    assert xreport.items_sold == {"apple": 4, "banana": 2, "orange": 4}

    empty_receipts: List[Receipt | None] = []
    empty_xreport = xreport_service.generate_x_report(shift_id, empty_receipts)
    assert empty_xreport.total_receipts == 0
    assert empty_xreport.revenue == 0.0
    assert empty_xreport.items_sold == {}

    none_receipts: List[Receipt | None] = [None]
    import pytest
    with pytest.raises(Exception, match="receipt is None"):
        xreport_service.generate_x_report(shift_id, none_receipts)