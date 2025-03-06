from collections import defaultdict
from typing import Any, Dict, Optional

from app.core.receipt import Receipt
from app.core.repository import Repository
from app.core.shift import Shift


class XReportService:
    def __init__(self, shift_repo: Repository[Shift],
                 receipt_repo: Repository[Receipt]) -> None:
        self.shift_repo = shift_repo
        self.receipt_repo = receipt_repo

    def generate_x_report(self, shift_id: str) -> Optional[Dict[str, Any]]:
        receipt_ids = self.shift_repo.get_shift_receipt_ids(shift_id)

        if not receipt_ids:
            return None

        receipts = self.receipt_repo.get_every_receipt(receipt_ids)

        total_receipts: int = len(receipts)
        item_sales: defaultdict[str, float] = defaultdict(float)
        revenue_by_currency: defaultdict[str, float] = defaultdict(float)

        for receipt in receipts:
            for item in receipt.products:
                item_sales[item.id] += item.quantity
                revenue_by_currency["USD"] += item.quantity * item.price

        return {
            "shift_id": shift_id,
            "total_receipts": total_receipts,
            "items_sold": item_sales,
            "revenue": revenue_by_currency,
        }