from __future__ import annotations

from typing import Protocol, List, Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.repository import Repository
from app.core.shift import Shift
from app.services.shift_service import ShiftService

shift_api = APIRouter()

class _Infra(Protocol):
    def shift(self) -> Repository[Shift]:
        pass

class ShiftModel(BaseModel):
    shift_id: str
    status: str
    receipts: List[str]

def create_shift_service(req: Request) -> ShiftService:
    infra: _Infra = req.app.state.infra
    return ShiftService(infra.shift())

@shift_api.post(
    "/{shift_id}/create",
    status_code=201,
    response_model=ShiftModel,
)
def create_shift(service: Annotated[ShiftService, Depends(create_shift_service)]) -> Shift:
    return service.create()

@shift_api.post(
    "",
    status_code=200,
    response_model=None,
)
def open_shift(service: Annotated[ShiftService, Depends(create_shift_service)]) -> None:
    service.open_shift()

@shift_api.post(
    "/{shift_id}/close",
    status_code=200,
    response_model=None,
)
def close_shift(shift_id: str, service: Annotated[ShiftService, Depends(create_shift_service)]) -> None:
    service.close_shift(shift_id)

@shift_api.post(
    "/{shift_id}/receipts/{receipt_id}",
    status_code=200,
    response_model=None,
)
def add_receipt_to_shift(
    shift_id: str, receipt_id: str,
    service: Annotated[ShiftService, Depends(create_shift_service)]
) -> None:
    service.add_receipt_to_shift(shift_id, receipt_id)