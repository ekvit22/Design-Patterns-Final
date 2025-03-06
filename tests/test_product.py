from typing import List, Optional

from app.core.product import Product
from app.core.repository import Repository
from app.infra.in_memory import InMemory
from app.schemas.product import CreateProductRequest, UpdateProductRequest
from app.services.product_service import ProductService


def test_should_make_product() -> None:
    product: Product = Product("123456","98765","pumpkin","55555",50)
    assert product.name == "pumpkin"
    assert product.price == 50
    assert product.id == "123456"
    assert product.unit == "98765"
    assert product.barcode == "55555"

def test_product_service_create() -> None:
    in_memory: InMemory = InMemory()
    service: ProductService = ProductService(in_memory.products())
    request = CreateProductRequest(unit="98765", name="pumpkin",
                                   barcode="55555", price=50)
    product: Product = service.create(request)
    assert product.name == "pumpkin"
    assert product.price == 50
    assert product.unit == "98765"
    assert product.barcode == "55555"

def test_product_service_read() -> None:
    in_memory: InMemory = InMemory()
    service: ProductService = ProductService(in_memory.products())
    request = CreateProductRequest(unit="98765", name="pumpkin",
                                   barcode="55555", price=50)
    product: Product = service.create(request)
    product = service.read(product.id)
    assert product.name == "pumpkin"
    assert product.price == 50
    assert product.unit == "98765"
    assert product.barcode == "55555"

def test_product_service_read_all() -> None:
    in_memory: InMemory = InMemory()
    service: ProductService = ProductService(in_memory.products())

    request1 = CreateProductRequest(unit="98765", name="pumpkin",
                                   barcode="55555", price=50)
    request2 = CreateProductRequest(unit="45654", name="potato",
                                   barcode="4444", price=30)

    product1: Product = service.create(request1)
    product2: Product = service.create(request2)
    products: List[Product] = service.read_products()
    assert products[0] == product1
    assert products[1] == product2

def test_product_service_update() -> None:
    in_memory: InMemory = InMemory()
    service: ProductService = ProductService(in_memory.products())
    request = CreateProductRequest(unit="98765",name="pumpkin",
                                   barcode="55555", price=50)
    product: Product = service.create(request)
    service.update_product(product.id,UpdateProductRequest(price=400))
    product = service.read(product.id)
    assert product.name == "pumpkin"
    assert product.price == 400
    assert product.unit == "98765"
    assert product.barcode == "55555"


def test_product_in_memory() -> None:
    products: Repository[Product] = InMemory().products()
    products.create(Product("12345","55555","pumpkin","8888",20))
    res: Optional[Product] = products.read("12345")
    assert res == Product("12345","55555","pumpkin","8888",20)

    res = products.read_with_barcode("8888")
    assert res == Product("12345", "55555", "pumpkin", "8888", 20)

    product_list: List[Product] = products.get_all()
    assert product_list[0] == Product("12345","55555","pumpkin","8888",20)

    products.update(Product("12345","55555","pumpkin","8888",400))
    res = products.read("12345")
    assert res is not None
    assert res.price == 400