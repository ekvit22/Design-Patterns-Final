from dataclasses import dataclass
from typing import List

from torch.fx.experimental.unification.unification_tools import getter


@dataclass
class Products:
    id: str
    quantity: int
    price: int
    total: int

@dataclass
class Receipt:
    id: str
    status: str
    products: List[Products]
    total: int