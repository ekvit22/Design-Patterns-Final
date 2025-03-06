from dataclasses import dataclass


@dataclass
class Product:
    id: str
    unit: str
    name: str
    price: float
    barcode: str
