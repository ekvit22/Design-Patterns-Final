from typing import Optional, List

from pydantic import BaseModel

from app.core.receipt import Products


class CreateReceiptRequest(BaseModel):
    status: str
    products: Optional[List[Products]] = []
    total: Optional[int] = 0