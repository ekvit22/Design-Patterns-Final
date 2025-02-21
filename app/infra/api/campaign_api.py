from __future__ import annotations

from typing import Annotated, List, Protocol

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.Repository import Repository
from app.core.campaign import Campaign
from app.schemas.campaign import CreateCampaignRequest
from app.services.campaign_service import CampaignService

campaigns_api = APIRouter()

class CampaignItem(BaseModel):
    id: str
    name: str
    type: str
    product_id: str
    products: list
    discount: int
    gift_id: str
    gift_required_count: int


class _Infra(Protocol):

    def campaigns(self) -> Repository[Campaign]:
        pass


def create_campaigns_service(
    request: Request
) -> CampaignService:
    infra: _Infra = request.app.state.infra

    return CampaignService(infra.campaigns())

@campaigns_api.post(
    "",
    status_code=201,
    response_model=CampaignItem,
)
def create_campaign(
        request: CreateCampaignRequest,
    service: Annotated[CampaignService, Depends(create_campaigns_service)],
) -> Campaign:
    return service.create(request)

@campaigns_api.delete(
    "/{campaign_id}",
    status_code=200,
    response_model=None,
)
def delete(
    campaign_id: str,
    service: Annotated[CampaignService, Depends(create_campaigns_service)],
) -> None:
   service.delete(campaign_id)


@campaigns_api.get(
    "",
    status_code=200,
    response_model=List[CampaignItem],
)
def read_units(
    service: Annotated[CampaignService, Depends(create_campaigns_service)],
) -> List[Campaign]:
    return service.read_campaigns()