from dataclasses import dataclass
from typing import List


@dataclass
class Shift:
    id: str
    status: str
    receipts: List[str]