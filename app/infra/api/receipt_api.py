from __future__ import annotations

from typing import Annotated, List, Protocol

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.Repository import Repository
from app.core.receipt import Receipt, Products
from app.schemas.receipt import CreateReceiptRequest
from app.services.receipt_service import ReceiptService

receipt_api = APIRouter()

class _Infra(Protocol):
    def receipt(self) -> Repository[Receipt]:
        pass

class ReceiptModel(BaseModel):
    id: str
    status: str
    products: List[Products]
    total: int

def create_receipt_service(req: Request) -> ReceiptService:
    infra: _Infra = req.app.state.infra
    return ReceiptService(infra.receipt())

@receipt_api.get(
    "",
    status_code=200,
    response_model=ReceiptModel,
)
def read_units(rec_id: str,
    service: Annotated[ReceiptService, Depends(create_receipt_service)],
) -> Receipt:
    return service.read(rec_id)
