from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class XReport:
    id: str
    shift_id: str
    total_receipts: int
    items_sold: Dict[str, int]
    revenue: float