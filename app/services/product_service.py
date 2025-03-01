import uuid
from typing import List

from fastapi import HTTPException

from app.core.product import Product
from app.core.repository import Repository
from app.schemas.product import CreateProductRequest, UpdateProductRequest


class ProductService:
    def __init__(self, repository: Repository[Product]):
        self.repository = repository

    def create(self, request: CreateProductRequest) -> Product:
        existing_product = self.repository.read_with_barcode(request.barcode)
        if existing_product is not None:
            raise HTTPException(
                status_code=409,
                detail={"error": {"message":
                        f"Product with barcode<{request.barcode}> already exists."}}
            )

        new_product = Product(id=str(uuid.uuid4()), **request.model_dump())

        self.repository.create(new_product)
        return new_product

    def read(self, product_id: str) -> Product:
        product = self.repository.read(product_id)
        if product is None:
            raise HTTPException(
                status_code=404,
                detail={"error": {"message":
                                f"Product with id<{product_id}> does not exist."}}
            )
        return product

    def read_products(self) -> List[Product]:
        return self.repository.get_all()

    def update_product(self,product_id: str, request: UpdateProductRequest) -> None:
        new_product = self.repository.read(product_id)
        if new_product is None:
            raise HTTPException(
                status_code=404,
                detail={"error": {"message":
                                f"Product with id<{product_id}> does not exist."}}
            )
        new_product.price = request.price
        self.repository.update(new_product)
