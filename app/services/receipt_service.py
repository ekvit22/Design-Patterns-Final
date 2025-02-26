import uuid
from http.client import HTTPException
from typing import List

from app.core.Repository import Repository
from app.core.receipt import Receipt
from app.core.receipt import Products
from app.schemas.receipt import CreateReceiptRequest

class ReceiptService:
    def __init__(self, repository: Repository[Receipt]):
        self.repository = repository

    def read(self, receipt_id: str) -> Receipt:
        receipt = self.repository.read(receipt_id)
        if receipt is None:
            raise HTTPException(
                status_code=404,
                detail={"error": {"message":
                                f"Receipt with id<{receipt_id}> does not exist."}}
            )
        return receipt

    

