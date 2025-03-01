from dataclasses import dataclass


@dataclass
class Product:
    id: str
    unit_id: str
    name: str
    price: int
    barcode: str
