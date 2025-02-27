from dataclasses import dataclass
from typing import List


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