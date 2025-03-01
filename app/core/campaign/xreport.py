from dataclasses import dataclass
from typing import Dict


@dataclass
class XReport:
    shift_id: str
    receipt_count: int
    items_sold: Dict[str, Dict[str, any]]
    revenue_total: int