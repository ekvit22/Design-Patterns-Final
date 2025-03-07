import uuid
from http.client import HTTPException
from typing import List, Optional

from app.core.repository import Repository
from app.core.shift import Shift


class ShiftService:
    def __init__(self, repository: Repository[Shift]) -> None:
        self.repository = repository

    def create(self) -> Shift:
        new_shift = Shift(id=str(uuid.uuid4()), status="open", receipts=[])
        self.repository.create(new_shift)
        return new_shift

    def open_shift(self, shift_id: str) -> None:
        shift = self.repository.read(shift_id)
        if not shift:
            raise ValueError(f"Shift {shift_id} does not exist.")
        self.repository.open_shift(shift_id)

    def close_shift(self, shift_id: str) -> None:
        shift = self.repository.read(shift_id)
        if not shift:
            raise ValueError(f"Shift {shift_id} does not exist.")
        self.repository.close_shift(shift_id)

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        shift = self.repository.read(shift_id)
        if not shift:
            raise ValueError(f"Shift {shift_id} does not exist.")
        return self.repository.get_shift_receipt_ids(shift_id)

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        shift = self.repository.read(shift_id)
        if not shift:
            raise ValueError(f"Shift {shift_id} does not exist.")
        if not self.repository.read(receipt_id):
            raise ValueError(f"Receipt {receipt_id} does not exist.")
        if shift.status != "open":
            raise ValueError(f"Cannot add receipt to a closed shift.")
        self.repository.add_receipt_to_shift(shift_id, receipt_id)

    def read_shift(self, shift_id: str) -> Optional[Shift]:
        return self.repository.read(shift_id)