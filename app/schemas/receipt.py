from pydantic import BaseModel

class AddProductRequest(BaseModel):
    id: str
    quantity: int

class ChangeReceiptRequest(BaseModel):
    status: str