import uuid
from http.client import HTTPException
from typing import List

from app.core.receipt import Receipt
from app.core.repository import Repository
from app.core.shift import Shift


class ShiftService:
    def __init__(self, repository: Repository[Shift]) -> None:
        self.repository = repository

    def create(self) -> Shift:
        new_receipt = Shift(id=str(uuid.uuid4()), status="open", receipts=[])
        self.repository.create(new_receipt)
        return new_receipt

    def open_shift(self, shift_id) -> None:
        self.repository.open_shift(shift_id)

    def close_shift(self, shift_id) -> None:
        self.repository.close_shift(shift_id)

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        # shift = self.repository.read(shift_id)
        # return shift.receipts
        # AN ANU AR VICI MCHIRDEBA VABSHE ES FUNQCIA
        return self.repository.get_shift_receipt_ids(shift_id)

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        shift = self.repository.read(shift_id)
        if shift.status == "open":
            shift.receipts.append(receipt_id)

    def read_shift(self, shift_id: str) -> Shift:
        return self.repository.read(shift_id)