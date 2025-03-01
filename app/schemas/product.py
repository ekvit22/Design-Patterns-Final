from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    unit_id: str
    name: str
    barcode: str
    price: int

class UpdateProductRequest(BaseModel):
    price: int