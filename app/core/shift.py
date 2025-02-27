from dataclasses import dataclass

from app.core.receipt import Receipt


@dataclass
class Shift:
    shift_id: str
    status: str
    receipts: list[Receipt]