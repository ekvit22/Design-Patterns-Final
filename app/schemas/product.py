from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    unit: str
    name: str
    barcode: str
    price: float

class UpdateProductRequest(BaseModel):
    price: float