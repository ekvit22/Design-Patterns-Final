from __future__ import annotations

from typing import Annotated, List, Protocol

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.receipt import Products, Receipt
from app.core.repository import Repository
from app.infra.api.campaign_api import create_campaigns_service
from app.infra.api.products import create_products_service
from app.infra.api.shift_api import create_shift_service
from app.schemas.receipt import AddProductRequest, ChangeReceiptRequest
from app.services.campaign_service import CampaignService
from app.services.product_service import ProductService
from app.services.receipt_service import ReceiptService
from app.services.shift_service import ShiftService

receipt_api = APIRouter()

class _Infra(Protocol):
    def receipts(self) -> Repository[Receipt]:
        pass

class ReceiptItem(BaseModel):
    id: str
    status: str
    products: List[Products]
    total: float

def create_receipt_service(req: Request) -> ReceiptService:
    infra: _Infra = req.app.state.infra
    return ReceiptService(infra.receipts())

@receipt_api.get(
    "/{receipt_id}",
    status_code=200,
    response_model=ReceiptItem,
)
def read_receipt(receipt_id: str,
    service: Annotated[ReceiptService, Depends(create_receipt_service)],
) -> Receipt:
    return service.read(receipt_id)

@receipt_api.get(
    "/{receipt_id}/discounted_price",
    status_code=200,
    response_model=float,
)
def get_discounted_price(receipt_id: str,
    receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)],
    campaign_service: Annotated[CampaignService, Depends(create_campaigns_service)],
    ) -> float:
    receipt = receipt_service.read(receipt_id)
    old_total = receipt_service.get_total(receipt)
    receipt = campaign_service.apply_campaigns(receipt)
    new_total = receipt_service.get_total(receipt)

    return old_total - new_total

@receipt_api.post(
    "/{receipt_id}/quotes",
    status_code=200,
    response_model=float,
)
def calculate_payment(receipt_id: str,
    currency: str,
    receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)],
    ) -> float:
    return receipt_service.calculate_payment(receipt_id, currency)

@receipt_api.post(
    "/{receipt_id}/payments",
    status_code=200,
    response_model=None,
)
def complete_payment(receipt_id: str,
    service: Annotated[ReceiptService, Depends(create_receipt_service)]) -> None:
    service.close_receipt(receipt_id)

@receipt_api.post(
    "",
    status_code=201,
    response_model=ReceiptItem,
)
def create_receipt(
    service: Annotated[ReceiptService, Depends(create_receipt_service)],
) -> Receipt:
    return service.create()

@receipt_api.post(
    "/{receipt_id}/products",
    status_code=200,
    response_model=ReceiptItem,
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

@receipt_api.get(
    "/{shift_id}/z_reports",
    status_code=200,
    response_model=List[ReceiptItem],
)
def get_z_reports(shift_id: str,
    receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)],
    shift_service: Annotated[ShiftService, Depends(create_shift_service)],
) -> List[Receipt]:
    receipt_ids = shift_service.get_shift_receipt_ids(shift_id)
    return receipt_service.get_every_receipt(receipt_ids)

