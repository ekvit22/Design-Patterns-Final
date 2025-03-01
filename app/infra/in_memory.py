from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, List, Optional, Protocol, TypeVar

from app.core.campaign.xreport import XReport
from app.core.product import Product
from app.core.receipt import Receipt
from app.core.repository import Repository
from app.core.campaign.campaign import Campaign
from app.core.shift import Shift
from app.schemas.sales import SalesData


class _Item(Protocol):
    id: str


ItemT = TypeVar("ItemT", bound=_Item)

@dataclass
class InMemoryRepository(Generic[ItemT]):
    items: list[ItemT] = field(default_factory=list)

    def create(self, item: ItemT) -> ItemT:
        self.items.append(item)

        return item

    def read(self, item_id: str) -> Optional[ItemT]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def read_with_name(self, item_name: str) -> Optional[ItemT]:
        for item in self.items:
            if hasattr(item, "name") and item.name == item_name:
                return item
        return None

    def update(self, item: ItemT) -> None:
        self.delete(item.id)
        self.create(item)

    def delete(self, item_id: str) -> None:
        self.items = [account for account in self.items if account.id != item_id]

    def get_all(self) -> list[ItemT]:
        return self.items

    def open_receipt(self, receipt_id: str) -> None:
        for item in self.items:
            if receipt_id == item.receipt_id:
                item.status = "open"
                break

    def close_receipt(self, receipt_id: str) -> None:
        for item in self.items:
            if receipt_id == item.receipt_id:
                item.status = "close"
                break

    def get_every_receipt(self, receipt_ids: List[str]) -> List[Receipt]:
        return [item for item in self.items if isinstance(item, Shift) and item.shift_id in receipt_ids]

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        shift = next((item for item in self.items if isinstance(item, Shift) and item.shift_id == shift_id), None)
        return shift.receipts if shift else []


    def open_shift(self, shift_id: str) -> None:
        for item in self.items:
            if item.shift_id == shift_id:
                item.status = "open"
                break

    def close_shift(self, shift_id: str) -> None:
        for item in self.items:
            if item.shift_id == shift_id:
                item.status = "closed"
                break

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        shift = self.read(shift_id)
        if shift.status == "open":
            shift.receipts.append(receipt_id)

    def read_with_barcode(self, barcode: str) -> Optional[ItemT]:
        for item in self.items:
            if hasattr(item, "barcode") and item.barcode == barcode:
                return item
        return None

    def get_sales_data(self) -> Optional[SalesData]:
        res: SalesData = SalesData(n_receipts=0, revenue=0)
        for item in self.items:
            if hasattr(item, "status") and item.status == "closed":
                res.n_receipts += 1
                if hasattr(item, "total"):
                    res.revenue += item.total
        return res


@dataclass
class InMemory:
    _campaigns: InMemoryRepository[Campaign] = field(
        init=False,
        default_factory=InMemoryRepository,
    )

    _receipts: InMemoryRepository[Receipt] = field(
        init=False,
        default_factory=InMemoryRepository,
    )

    _shifts: InMemoryRepository[Shift] = field(
        init=False,
        default_factory=InMemoryRepository
    )

    _products: InMemoryRepository[Product] = field(
        init=False,
        default_factory=InMemoryRepository,
    )

    _xreport: InMemoryRepository[XReport] = field(
        init=False,
        default_factory=InMemoryRepository,
    )


    def campaigns(self) -> Repository[Campaign]:
        return self._campaigns

    def receipts(self) -> Repository[Receipt]:
        return self._receipts

    def shifts(self) -> Repository[Shift]:
        return self._shifts

    def products(self) -> Repository[Product]:
        return self._products

    def xreport(self) -> Repository[XReport]:
        return self._xreport