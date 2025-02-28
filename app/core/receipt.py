from dataclasses import dataclass
from typing import List



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