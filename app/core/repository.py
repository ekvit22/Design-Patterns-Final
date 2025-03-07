from typing import List, Optional, Protocol, TypeVar

from app.core.receipt import Products, Receipt
from app.schemas.sales import SalesData

ItemT = TypeVar("ItemT")


class Repository(Protocol[ItemT]):
    def create(self, item: ItemT) -> ItemT:
        pass

    def read(self, item_id: str) -> Optional[ItemT]:
        pass

    def read_with_name(self, item_name: str) -> Optional[ItemT]:
        pass

    def update(self, item: ItemT) -> None:
        pass

    def delete(self, item_id: str) -> None:
        pass

    def get_all(self) -> List[ItemT]:
        pass

    def open_receipt(self, receipt_id: str) -> None:
        pass

    def close_receipt(self, receipt_id: str) -> None:
        pass

    def get_every_receipt(self, receipt_ids: List[str]) -> List[ItemT]:
        pass

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        pass

    def open_shift(self, shift_id: str) -> None:
        pass

    def close_shift(self, shift_id : str) -> None:
        pass

    def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
        pass

    def read_with_barcode(self, item_barcode: str) -> Optional[ItemT]:
        pass

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        pass

    def get_sales_data(self) -> Optional[SalesData]:
        pass