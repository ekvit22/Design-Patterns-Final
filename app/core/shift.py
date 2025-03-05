from dataclasses import dataclass
from typing import List

from app.core.receipt import Receipt


@dataclass
class Shift:
    id: str
    status: str
    receipts: List[str]