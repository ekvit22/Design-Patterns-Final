from typing import Optional, List

from pydantic import BaseModel

from app.core.receipt import Products


class GetDiscountRequest(BaseModel):
    products: List[Products]
    total: int