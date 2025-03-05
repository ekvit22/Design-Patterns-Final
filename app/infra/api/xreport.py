from typing import Annotated, Protocol

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette.requests import Request

from app.core.campaign.xreport import XReport
from app.core.repository import Repository
from app.services.xreport_service import XReportService

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
