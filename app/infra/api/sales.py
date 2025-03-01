from __future__ import annotations

from typing import Annotated, Protocol

from fastapi import APIRouter
from fastapi.params import Depends

from app.core.receipt import Receipt
from app.core.repository import Repository
from app.infra.api.receipt_api import create_receipt_service
from app.schemas.sales import SalesData
from app.services.receipt_service import ReceiptService

sales_api =  APIRouter()


class _Infra(Protocol):
    def receipts(self) -> Repository[Receipt]:
        pass

@sales_api.get(
    "",
    status_code=200,
    response_model=SalesData,
)
def get_sales_data(
    service: Annotated[ReceiptService, Depends(create_receipt_service)],
) -> SalesData:
    return service.get_sales_data()