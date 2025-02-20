from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, List, Optional, Protocol, TypeVar

from app.core.product import Product
from app.core.receipt import Receipt
from app.core.Repository import Repository
from app.core.unit import Unit
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



@dataclass
class InMemory:
    _units: InMemoryRepository[Unit] = field(
        init=False,
        default_factory=InMemoryRepository,
    )

    _products: InMemoryRepository[Product] = field(
        init=False,
        default_factory=InMemoryRepository,
    )

    _receipts: InMemoryRepository[Receipt] = field(
        init=False,
        default_factory=InMemoryRepository,
    )

    def units(self) -> Repository[Unit]:
        return self._units

    def products(self) -> Repository[Product]:
        return self._products

    def receipts(self) -> Repository[Receipt]:
        return self._receipts