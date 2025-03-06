from typing import Optional

from app.core.receipt import Receipt
from app.core.repository import Repository
from app.core.shift import Shift
from fastapi import HTTPException

from app.core.xreport import XReport


class XReportService:
    def __init__(self, repository: Repository[XReport], shift_repository: Repository[Shift], receipt_repository: Repository[Receipt]):
        self.repository = repository
        self.shift_repository = shift_repository
        self.receipt_repository = receipt_repository

    def generate_x_report(self, shift_id: str, shift: Optional[Shift], receipt_repository: Optional[Repository[Receipt]]) -> XReport:
        shift = self.shift_repository.read(shift_id)
        if not shift:
            raise HTTPException(
                status_code=404,
                detail={"error": {"message": f"Shift with id<{shift_id}> does not exist. fuck"}}
            )

        report = self.repository.generate_x_report(shift_id, shift, self.receipt_repository)
        if not report:
            raise HTTPException(
                status_code=404,
                detail={"error": {
                    "message": f"Could not generate X-report for shift<{shift_id}>. The shift may not have any receipts. esaaa?"}}
            )

        return report