from __future__ import annotations

from typing import Annotated, List, Protocol

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.Repository import Repository
from app.core.receipt import Receipt, Products
from app.schemas.receipt import GetDiscountRequest
from app.services.campaign_service import CampaignService
from app.services.receipt_service import ReceiptService
from app.infra.api.campaign_api import create_campaigns_service

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
def read_receipt(rec_id: str,
    service: Annotated[ReceiptService, Depends(create_receipt_service)],
) -> Receipt:
    return service.read(rec_id)

@receipt_api.get(
    "",
    status_code=200,
    response_model=int,
)
def get_discount(receipt_id: str,
    receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)],
    campaign_service: Annotated[CampaignService, Depends(create_campaigns_service)],
    ) -> int:
    receipt = receipt_service.read(receipt_id)
    old_total = receipt_service.get_total(receipt)
    receipt = campaign_service.apply_campaigns(receipt)
    new_total = receipt_service.get_total(receipt)

    return old_total - new_total



