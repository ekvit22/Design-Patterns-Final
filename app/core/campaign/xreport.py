from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class XReport:
    shift_id: str
    receipt_count: int
    items_sold: Dict[str, Optional[Dict[str, Any]]]
    revenue_total: int