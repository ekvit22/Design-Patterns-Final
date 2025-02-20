from dataclasses import dataclass


@dataclass
class Campaign:
    id: str
    type: str
    product_id: str #for discounts and buy n get n
    products: list #for combos
    discount: int #for discount and combos
    gift_id: str #for get n
    gift_required_count: int #for buy n
