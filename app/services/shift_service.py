import uuid
from typing import List, Optional

from app.core.repository import Repository
from app.core.shift import Shift


class ShiftService:
    def __init__(self, repository: Repository[Shift]) -> None:
        self.repository = repository

    def create(self) -> Shift:
        new_receipt = Shift(id=str(uuid.uuid4()), status="open", receipts=[])
        self.repository.create(new_receipt)
        return new_receipt

    def open_shift(self, shift_id: str) -> None:
        self.repository.open_shift(shift_id)

    def close_shift(self, shift_id: str) -> None:
        self.repository.close_shift(shift_id)

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        return self.repository.get_shift_receipt_ids(shift_id)

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        self.repository.add_receipt_to_shift(shift_id, receipt_id)

    def read_shift(self, shift_id: str) -> Optional[Shift]:
        return self.repository.read(shift_id)