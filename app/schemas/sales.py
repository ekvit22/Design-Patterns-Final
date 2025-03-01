from pydantic import BaseModel


class SalesData(BaseModel):
    n_receipts: int
    revenue: int