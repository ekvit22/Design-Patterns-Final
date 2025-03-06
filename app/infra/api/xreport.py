from __future__ import annotations

from typing import Protocol, Annotated, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.repository import Repository
from app.core.shift import Shift
from app.core.xreport import XReport
from app.infra.api.receipt_api import create_receipt_service
from app.infra.api.shift_api import create_shift_service
from app.services.receipt_service import ReceiptService
from app.services.shift_service import ShiftService
from app.services.xreport_service import XReportService

xreport_api = APIRouter()


class _Infra(Protocol):
    def xreport(self) -> Repository[XReport]:
        pass


class XReportResponse(BaseModel):
    id: str
    shift_id: str
    total_receipts: int
    items_sold: Dict[str, int]
    revenue: float


def create_xreport_service(req: Request,
                           shift_service: Annotated[ShiftService, Depends(create_shift_service)],
                           receipt_service: Annotated[ReceiptService, Depends(create_receipt_service)]) -> XReportService:
    infra: _Infra = req.app.state.infra
    return XReportService(infra.xreport(), shift_service.repository, receipt_service.repository)


@xreport_api.get(
    "/{shift_id}",
    status_code=200,
    response_model=XReportResponse,
)
def get_x_report(
        shift_id: str,
        service: Annotated[XReportService, Depends(create_xreport_service)],
) -> XReport:
    return service.generate_x_report(shift_id, None, None)