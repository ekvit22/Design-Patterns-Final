from __future__ import annotations

from typing import Annotated, List, Protocol

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.repository import Repository
from app.core.receipt import Receipt, Products
from app.schemas.receipt import ChangeReceiptRequest, AddProductRequest
from app.services.campaign_service import CampaignService
from app.services.receipt_service import ReceiptService
from app.infra.api.campaign_api import create_campaigns_service
from app.core.constants import GEL, USD, EUR

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
    "/receipts/{receipt_id}",
    status_code=200,
    response_model=int,
)
def get_discounted_price(receipt_id: str,
    receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)],
    campaign_service: Annotated[CampaignService, Depends(create_campaigns_service)],
    ) -> int:
    receipt = receipt_service.read(receipt_id)
    old_total = receipt_service.get_total(receipt)
    receipt = campaign_service.apply_campaigns(receipt)
    new_total = receipt_service.get_total(receipt)

    return old_total - new_total

@receipt_api.post(
    "/receipts/{receipt_id}/quotes",
    status_code=200,
    response_model=int,
)
def calculate_payment(receipt_id: str,
    currency: str,
    receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)],
    ) -> int:
    return receipt_service.calculate_payment(receipt_id, currency)

@receipt_api.post(
    "/receipts",
    status_code=201,
    response_model=ReceiptModel,
)
def create_receipt(
    service: Annotated[ReceiptService, Depends(create_receipt_service)],
) -> Receipt:
    return service.create()

@receipt_api.post(
    "/{receipt_id}/products",
    status_code=200,
    response_model=ReceiptModel,
)
def add_product(
    receipt_id: str,
    request: AddProductRequest,
    receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)],
    product_service: Annotated[ProductService, Depends(create_products_service)],
) -> Receipt:
    product: Products = product_service.read(request.id)
    return receipt_service.add_product(receipt_id, product, request)

@receipt_api.patch(
    "/{receipt_id}",
    status_code=200,
    response_model=None,
)
def update_receipt_status(
    receipt_id: str,
    request: ChangeReceiptRequest,
    service: Annotated[ReceiptService, Depends(create_receipt_service)],
) -> None:
    if request.status == "open":
        service.open_receipt(receipt_id)
    else:
        service.close_receipt(receipt_id)

# @receipts_api.get(
#     "/z_report",
#     status_code=200,
#     response_model=Optional[ReceiptItem],
# )
# def read_receipts(
#     service: Annotated[ReceiptService, Depends(create_receipts_service)],
# ) -> list[Receipt]:
#     return service

