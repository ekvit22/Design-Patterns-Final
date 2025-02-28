from dataclasses import dataclass
from typing import Optional


@dataclass
class Campaign:
    id: str
    name: str
    description: str
    # type: str
    # product_id: str #for discounts and buy n get n
    # products: list #for combos
    # discount: int #for discount and combos
    # gift_id: str #for get n
    # gift_required_count: int #for buy n

    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
