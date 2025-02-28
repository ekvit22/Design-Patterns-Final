from dataclasses import dataclass
from typing import List

from app.core.receipt import Receipt


@dataclass
class Shift:
    shift_id: str
    status: str
    receipts: List[str]