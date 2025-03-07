from typing import List
from uuid import uuid4

from app.core.receipt import Receipt
from app.core.repository import Repository
from app.core.shift import Shift

from app.core.xreport import XReport


class XReportService:
    def __init__(self, repository: Repository[XReport], shift_repository: Repository[Shift], receipt_repository: Repository[Receipt]):
        self.repository = repository
        self.shift_repository = shift_repository
        self.receipt_repository = receipt_repository

    def generate_x_report(self, shift_id: str, receipts: List[Receipt | None]) -> XReport:
        total_receipts = len(receipts)
        items_sold: dict[str, int] = {}
        revenue = 0.0

        for receipt in receipts:
            if receipt is None:
                raise Exception('receipt is None')
            revenue += receipt.total
            for product in receipt.products:
                items_sold[product.id] = items_sold.get(product.id, 0) + product.quantity

        return XReport(
            id=str(uuid4()),
            shift_id=shift_id,
            total_receipts=total_receipts,
            items_sold=items_sold,
            revenue=revenue
        )