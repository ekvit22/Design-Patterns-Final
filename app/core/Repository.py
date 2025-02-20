from typing import List, Optional, Protocol, TypeVar

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