from typing import List

from pydantic import BaseModel

from app.core.receipt import Products


class AddProductRequest(BaseModel):
    id: str
    quantity: int

class ChangeReceiptRequest(BaseModel):
    status: str