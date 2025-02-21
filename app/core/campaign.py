from dataclasses import dataclass
from typing import Optional


@dataclass
class Campaign:
    id: str
    name: str
    type: str
    product_id: str #for discounts and buy n get n
    products: list #for combos
    discount: int #for discount and combos
    gift_id: str #for get n
    gift_required_count: int #for buy n

    def __init__(self, id: str, name: str, type: str, product_id: str = "", products: Optional[list] = None, discount: int = 0, gift_id: str = "", gift_required_count: int = 0):
        if products is None:
            products = []
        self.id = id
        self.name = name
        self.type = type
        self.product_id = product_id
        self.products = products
        self.discount = discount
        self.gift_id = gift_id
        self.gift_required_count = gift_required_count
