from __future__ import annotations

from typing import Annotated, List, Protocol

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request

from app.core.product import Product
from app.core.repository import Repository
from app.schemas.product import CreateProductRequest, UpdateProductRequest
from app.services.product_service import ProductService


products_api = APIRouter()

class ProductItem(BaseModel):
    id: str
    unit: str
    name: str
    barcode: str
    price: float

class _Infra(Protocol):
    def products(self) -> Repository[Product]:
        pass


def create_products_service(
    request: Request
) -> ProductService:
    infra: _Infra = request.app.state.infra

    return ProductService(infra.products())

@products_api.post(
    "",
    status_code=201,
    response_model=ProductItem,
)
def create_product(
        request: CreateProductRequest,
    service: Annotated[ProductService, Depends(create_products_service)],
) -> Product:
    return service.create(request)

@products_api.get(
    "/{product_id}",
    status_code=200,
    response_model=ProductItem,
)
def read_product(
    product_id: str,
    service: Annotated[ProductService, Depends(create_products_service)],
) -> Product:
    return service.read(product_id)


@products_api.patch(
    "/{product_id}",
    status_code=200,
    response_model=None,
)
def update_product(
        product_id: str,
        request: UpdateProductRequest,
        service: Annotated[ProductService, Depends(create_products_service)],
) -> None:
    service.update_product(product_id, request)


@products_api.get(
    "",
    status_code=200,
    response_model=List[ProductItem],
)
def read_products(
    service: Annotated[ProductService, Depends(create_products_service)],
) -> List[Product]:
    return service.read_products()
