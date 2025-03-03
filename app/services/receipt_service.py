import uuid
from http.client import HTTPException
from typing import List, Optional

from app.core.repository import Repository
from app.core.receipt import Receipt
from app.core.receipt import Products
from app.schemas.receipt import AddProductRequest
from app.core.constants import GEL, USD, EUR, GEL_TO_USD, GEL_TO_EUR
from app.schemas.sales import SalesData


class ReceiptService:
    def __init__(self, repository: Repository[Receipt]) -> None:
        self.repository = repository

    def create(self) -> Receipt:
        new_receipt = Receipt(id=str(uuid.uuid4()), status="open", products=[], total=0)
        self.repository.create(new_receipt)
        return new_receipt

    def read(self, receipt_id: str) -> Receipt:
        receipt = self.repository.read(receipt_id)
        if receipt is None:
            raise HTTPException(
                status_code=404,
                detail={"error": {"message":
                                f"Receipt with id<{receipt_id}> does not exist."}}
            )
        return receipt

    #getter
    def get_total(self, receipt: Receipt) -> int:
        return receipt.total

    def open_receipt(self, receipt_id: str) -> None:
        self.repository.open_receipt(receipt_id)

    def close_receipt(self, receipt_id: str) -> None:
        self.repository.close_receipt(receipt_id)

    # AQ MAINTERESEBS TOTALS AQ XELIT UNDA GAVZARDO TU RAGDAN SQLITESHI MIWERIA AR MIDNA VKITXO BENDOS
    def add_product(self, receipt_id: str, product: Products, request: AddProductRequest) -> Receipt:
        new_receipt: Optional[Receipt] = self.repository.read(receipt_id)
        if new_receipt is None:
            raise HTTPException(status_code=404,
                detail={"error":{"message":
                                f"Receipt with id<{receipt_id}> does not exist."}})
        product_price = product.price
        product_total = product_price*request.quantity
        added_product = Products(request.id, request.quantity, product_price, product_total)
        new_receipt.products.append(added_product)
        new_receipt.total += product_total
        self.repository.update(new_receipt)
        return new_receipt

    # AR VIYENEB
    def get_all(self) -> List[Receipt]:
        items = self.repository.get_all()
        if items is None:
            raise HTTPException(status_code=404,
                detail={"error":{"message":
                                "Receipts don't exist."}})
        return items

    def get_every_receipt(self, receipt_ids: List[str]) -> List[Receipt]:
        receipts = []
        for receipt_id in receipt_ids:
            receipt = self.repository.read(receipt_id)
            receipts.append(receipt)
        return receipts

    def calculate_payment(self, receipt_id: str, currency: str) -> float:
        receipt = self.repository.read(receipt_id)
        total = receipt.total

        if currency == USD:
            return self.change_currency(total, GEL_TO_USD)
        elif currency == EUR:
            return self.change_currency(total, GEL_TO_EUR)

        return total

    def change_currency(self, total: float, exchange_rate: float) -> float:
        return total / exchange_rate

    def get_sales_data(self) -> SalesData:
        res: Optional[SalesData] = self.repository.get_sales_data()
        if res is None:
            raise HTTPException(status_code=404,
                                detail={"error": {"message":
                                                      "Something went wrong"}}
                                )
        return SalesData(n_receipts=res.n_receipts, revenue=res.revenue)

