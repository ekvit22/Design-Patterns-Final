from dataclasses import dataclass

from app.core.receipt import Receipt


@dataclass
class Shift:
    id: str
    status: str
    receipts: list[Receipt]