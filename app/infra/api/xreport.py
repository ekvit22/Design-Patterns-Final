from typing import Protocol, Annotated

from fastapi import APIRouter, HTTPException

from app.core.campaign.xreport import XReport
from app.core.repository import Repository
from app.infra.api.shift_api import create_shift_service
from app.infra.sqlite import Sqlite
from app.services.receipt_service import ReceiptService
from app.services.shift_service import ShiftService
from app.services.xreport_service import XReportService
from starlette.requests import Request
from fastapi.params import Depends

xreport_api = APIRouter()

class _Infra(Protocol):
    def shift(self) -> Repository[XReport]:
        pass

def create_x_report_service(
    request: Request
) -> XReportService:
    infra: _Infra = request.app.state.infra

    return XReportService(infra.shifts(), infra.receipts())

@xreport_api.get("/{shift_id}", status_code=200)
def get_x_report(
    shift_id: str,
    service: Annotated[XReportService, Depends(create_x_report_service)],
):
    report = service.generate_x_report(shift_id)

    if not report:
        raise HTTPException(status_code=404, detail=f"Shift with ID {shift_id} not found")

    return report
