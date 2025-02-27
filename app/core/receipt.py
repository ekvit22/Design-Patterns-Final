from dataclasses import dataclass
from typing import List

from torch.fx.experimental.unification.unification_tools import getter


@dataclass
class Products:
    product_id: str
    quantity: int
    price: int
    total: int

@dataclass
class Receipt:
    receipt_id: str
    status: str
    products: List[Products]
    total: int