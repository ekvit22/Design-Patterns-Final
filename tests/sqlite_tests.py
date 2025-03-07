import uuid
from typing import List, Optional

from app.core.campaign.campaign import Campaign
from app.core.product import Product
from app.core.receipt import Products, Receipt
from app.core.repository import Repository
from app.core.shift import Shift
from app.core.xreport import XReport
from app.infra.sqlite import Sqlite
from app.schemas.sales import SalesData
from app.services.receipt_service import ReceiptService



def test_campaign_sql_memory() -> None:
    campaigns: Repository[Campaign] = Sqlite().campaigns()
    campaign1 = Campaign("4444","test1","discount;1234;10")
    campaign2 = Campaign("333", "test2", "combo;1234|12345;10")
    campaigns.create(campaign1)
    campaigns.create(campaign2)

    res = campaigns.get_all()
    assert len(res) == 2
    assert res[0].id == campaign1.id
    assert res[1].id == campaign2.id

    camp = campaigns.read(campaign1.id)
    if camp is None:
        raise Exception("campaign not found")
    assert camp.id == campaign1.id

    camp = campaigns.read_with_name(campaign1.name)
    if camp is None:
        raise Exception("campaign not found")
    assert camp.id == campaign1.id

    campaigns.delete(campaign1.id)

    res = campaigns.get_all()
    assert len(res) == 1
    assert res[0].id == campaign2.id


def test_product_sql_memory() -> None:
    products: Repository[Product] = Sqlite().products()
    products.create(Product("1234","55555","pumpkin","8888",20))
    res: Optional[Product] = products.read("1234")
    assert res == Product("1234","55555","pumpkin","8888",20)

    res = products.read_with_barcode("8888")
    assert res == Product("1234", "55555", "pumpkin", "8888", 20)

    product_list: List[Product] = products.get_all()
    assert product_list[0] == Product("1234","55555","pumpkin","8888",20)

    products.update(Product("1234","55555","pumpkin","8888",400))
    res = products.read("1234")
    assert res is not None
    assert res.price == 400


def test_xreport_generation() -> None:
    from app.infra.sqlite import Sqlite
    from app.services.xreport_service import XReportService
    from uuid import uuid4

    sqlite = Sqlite()
    sqlite.clear_tables()

    shift_repo = sqlite.shifts()
    receipt_repo = sqlite.receipts()
    product_repo = sqlite.products()

    class MockXReportRepository(Repository[XReport]):
        def create(self, item: XReport) -> XReport:
            return item

        def read(self, item_id: str) -> Optional[XReport]:
            return None

        def update(self, item: XReport) -> None:
            pass

        def delete(self, item_id: str) -> None:
            pass

        def get_all(self) -> List[XReport]:
            return []

        def read_with_name(self, item_name: str) -> Optional[XReport]:
            return None

        def read_with_barcode(self, item_barcode: str) -> Optional[XReport]:
            return None

        def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
            pass

        def close_receipt(self, receipt_id: str) -> None:
            pass

        def open_receipt(self, receipt_id: str) -> None:
            pass

        def close_shift(self, shift_id: str) -> None:
            pass

        def open_shift(self, shift_id: str) -> None:
            pass

        def get_every_receipt(self, receipt_ids: List[str]) -> List[XReport]:
            return []

        def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
            return []

        def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
            return []

        def get_sales_data(self) -> Optional[SalesData]:
            return None

    product1 = Product("p1", "unit", "Product 1", "1111", 10.0)
    product2 = Product("p2", "unit", "Product 2", "2222", 15.0)
    product_repo.create(product1)
    product_repo.create(product2)

    shift_id = str(uuid4())
    shift = Shift(id=shift_id, status="open", receipts=[])
    shift_repo.create(shift)

    receipt1_id = str(uuid4())
    receipt1 = Receipt(
        id=receipt1_id,
        status="close",
        products=[
            Products(id="p1", quantity=2, price=10.0, total=20.0),
            Products(id="p2", quantity=1, price=15.0, total=15.0)
        ],
        total=35.0
    )

    receipt2_id = str(uuid4())
    receipt2 = Receipt(
        id=receipt2_id,
        status="close",
        products=[
            Products(id="p1", quantity=1, price=10.0, total=10.0),
            Products(id="p2", quantity=3, price=15.0, total=45.0)
        ],
        total=55.0
    )

    receipt_repo.create(receipt1)
    receipt_repo.create(receipt2)
    shift_repo.add_receipt_to_shift(shift_id, receipt1_id)
    shift_repo.add_receipt_to_shift(shift_id, receipt2_id)

    xreport_service = XReportService(MockXReportRepository(), shift_repo, receipt_repo)

    shift_with_receipts = shift_repo.read(shift_id)
    assert shift_with_receipts is not None

    receipts = receipt_repo.get_every_receipt(shift_with_receipts.receipts)

    receipts_for_xreport: List[Receipt | None] = [receipt for receipt in receipts]

    xreport = xreport_service.generate_x_report(shift_id, receipts_for_xreport)

    assert xreport.shift_id == shift_id
    assert xreport.total_receipts == 2
    assert xreport.revenue == 90.0
    assert xreport.items_sold == {"p1": 3, "p2": 4}

def test_create_and_read_receipt() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()
    receipt = Receipt(id="receipt-1", status="open", products=[], total=0.0)
    receipt_repo.create(receipt)

    read_receipt = receipt_repo.read(receipt.id)
    assert read_receipt is not None
    assert read_receipt.id == "receipt-1"
    assert read_receipt.status == "open"
    assert read_receipt.total == 0.0

def test_update_receipt() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()
    receipt = Receipt(id="receipt-1", status="open", products=[], total=0.0)
    receipt_repo.create(receipt)

    product1 = Products(id="product-1", quantity=2, price=10.0, total=20.0)
    product2 = Products(id="product-2", quantity=3, price=40.0, total=120.0)
    new_receipt = receipt_repo.read(receipt.id)
    new_receipt.status = "close"
    new_receipt.products.append(product1)
    new_receipt.products.append(product2)
    new_receipt.total += product1.total + product2.total
    receipt_repo.update(new_receipt)
    updated_receipt = receipt_repo.read(new_receipt.id)
    assert updated_receipt is not None
    assert len(updated_receipt.products) == 2
    assert updated_receipt.products[0].id == "product-1"
    assert updated_receipt.total == 140.0

def test_delete_receipt() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()
    receipt = Receipt(id="receipt-1", status="open", products=[], total=0.0)
    receipt_repo.create(receipt)
    updated_receipt = receipt_repo.read(receipt.id)
    assert updated_receipt is not None
    assert updated_receipt.id == "receipt-1"

    receipt_repo.delete(receipt.id)
    deleted_receipt = receipt_repo.read(receipt.id)
    assert deleted_receipt is None

def test_open_receipt() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()
    receipt = Receipt(id="receipt-1", status="close", products=[], total=0.0)
    receipt_repo.create(receipt)
    read_receipt = receipt_repo.read(receipt.id)
    assert read_receipt.status == "close"
    receipt_repo.open_receipt(read_receipt.id)
    updated_receipt = receipt_repo.read(receipt.id)
    assert updated_receipt.status == "open"

def test_close_receipt() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()
    receipt = Receipt(id="receipt-1", status="open", products=[], total=0.0)
    receipt_repo.create(receipt)
    read_receipt = receipt_repo.read(receipt.id)
    assert read_receipt.status == "open"
    receipt_repo.close_receipt(read_receipt.id)
    updated_receipt = receipt_repo.read(receipt.id)
    assert updated_receipt.status == "close"

def test_get_every_receipt() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()
    receipt1 = Receipt(id="receipt-1", status="open", products=[], total=50.0)
    receipt2 = Receipt(id="receipt-2", status="closed", products=[], total=100.0)
    receipt_repo.create(receipt1)
    receipt_repo.create(receipt2)
    receipts = receipt_repo.get_every_receipt([receipt1.id, receipt2.id])
    assert len(receipts) == 2
    assert receipts[0].id == "receipt-1"
    assert receipts[1].id == "receipt-2"

def test_get_products_from_receipt() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()
    product1 = Products(id="product-1", quantity=2, price=5.0, total=10.0)
    product2 = Products(id="product-2", quantity=3, price=30.0, total=90.0)
    receipt = Receipt(id="receipt-1", status="open", products=[product1, product2], total=100.0)
    receipt_repo.create(receipt)
    products = receipt_repo.get_products_from_receipt(receipt.id)
    assert len(products) == 2
    assert products[0].id == "product-1"
    assert products[1].total == 90.0

def test_create_and_read_shift() -> None:
    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift = Shift(id="shift-1", status="open", receipts=[])
    shift_repo.create(shift)
    read_shift = shift_repo.read(shift.id)
    assert read_shift is not None
    assert read_shift.id == "shift-1"
    assert read_shift.status == "open"
    assert read_shift.receipts == []

def test_open_shift() -> None:
    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift = Shift(id="shift-1", status="closed", receipts=[])
    shift_repo.create(shift)
    assert shift_repo.read(shift.id).status == "closed"
    shift_repo.open_shift(shift.id)
    assert shift_repo.read(shift.id).status == "open"

def test_close_shift() -> None:
    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift = Shift(id="shift-1", status="open", receipts=[])
    shift_repo.create(shift)
    assert shift_repo.read(shift.id).status == "open"
    shift_repo.close_shift(shift.id)
    assert shift_repo.read(shift.id).status == "close"

def test_add_receipt_to_shift() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()

    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift = Shift(id="shift-1", status="open", receipts=[])
    shift_repo.create(shift)

    receipt = Receipt(id="receipt-1", status="open", products=[], total=50.0)
    receipt_repo.create(receipt)

    shift_repo.add_receipt_to_shift(shift.id, receipt.id)
    updated_shift = shift_repo.read(shift.id)
    assert "receipt-1" in updated_shift.receipts


def test_get_shift_receipt_ids() -> None:
    receipt_repo: Repository[Receipt] = Sqlite().receipts()

    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift = Shift(id="shift-1", status="open", receipts=[])
    shift_repo.create(shift)

    receipt1 = Receipt(id="receipt-1", status="open", products=[], total=50.0)
    receipt2 = Receipt(id="receipt-2", status="closed", products=[], total=100.0)
    receipt_repo.create(receipt1)
    receipt_repo.create(receipt2)

    shift_repo.add_receipt_to_shift(shift.id, receipt1.id)
    shift_repo.add_receipt_to_shift(shift.id, receipt2.id)
    receipt_ids = shift_repo.get_shift_receipt_ids(shift.id)
    assert len(receipt_ids) == 2
    assert "receipt-1" in receipt_ids
    assert "receipt-2" in receipt_ids


def test_update_shift() -> None:
    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift = Shift(id="shift-1", status="open", receipts=[])
    shift_repo.create(shift)
    new_shift = shift_repo.read(shift.id)
    new_shift.status = "close"
    shift_repo.update(new_shift)
    updated_shift = shift_repo.read("shift-1")
    assert updated_shift.status == "close"
    assert updated_shift.id == "shift-1"


def test_delete_shift() -> None:
    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift = Shift(id="shift-1", status="open", receipts=[])
    shift_repo.create(shift)
    assert shift_repo.read(shift.id) is not None
    shift_repo.delete(shift.id)
    assert shift_repo.read("shift-1") is None

def test_get_all_shifts() -> None:
    shift_repo: Repository[Shift] = Sqlite().shifts()
    shift1 = Shift(id="shift-1", status="open", receipts=[])
    shift2 = Shift(id="shift-2", status="closed", receipts=[])
    shift_repo.create(shift1)
    shift_repo.create(shift2)
    shifts = shift_repo.get_all()
    assert len(shifts) == 2
    assert shifts[0].id == "shift-1"
    assert shifts[1].id == "shift-2"

def test_sales_data_from_receipts() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    receipt_repo = sqlite.receipts()

    receipt1_id = str(uuid.uuid4())
    receipt1 = Receipt(
        id=receipt1_id,
        status="close",
        products=[
            Products(id="p1", quantity=2, price=10.0, total=20.0),
            Products(id="p2", quantity=1, price=15.0, total=15.0)
        ],
        total=35.0
    )

    receipt2_id = str(uuid.uuid4())
    receipt2 = Receipt(
        id=receipt2_id,
        status="close",
        products=[
            Products(id="p1", quantity=1, price=10.0, total=10.0),
            Products(id="p3", quantity=3, price=20.0, total=60.0)
        ],
        total=70.0
    )

    receipt_repo.create(receipt1)
    receipt_repo.create(receipt2)

    sales_data = receipt_repo.get_sales_data()
    assert sales_data is not None
    assert sales_data.n_receipts == 2
    assert sales_data.revenue == 105.0


def test_receipt_service_sales_data() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    receipt_repo = sqlite.receipts()
    receipt_service = ReceiptService(receipt_repo)

    receipt1 = Receipt(id=str(uuid.uuid4()), status="close", products=[], total=25.5)
    receipt2 = Receipt(id=str(uuid.uuid4()), status="close", products=[], total=42.75)
    receipt3 = Receipt(id=str(uuid.uuid4()), status="close", products=[], total=100.0)

    receipt_repo.create(receipt1)
    receipt_repo.create(receipt2)
    receipt_repo.create(receipt3)

    sales_data = receipt_service.get_sales_data()

    assert sales_data.n_receipts == 3
    assert sales_data.revenue == 168.25


def test_sales_data_with_product_additions() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    receipt_repo = sqlite.receipts()
    product_repo = sqlite.products()
    receipt_service = ReceiptService(receipt_repo)

    product1 = Product("p1", "unit", "Product 1", "1111", 10.0)
    product2 = Product("p2", "unit", "Product 2", "2222", 15.0)
    product_repo.create(product1)
    product_repo.create(product2)

    receipt = receipt_service.create()

    from app.schemas.receipt import AddProductRequest
    receipt_service.add_product(
        receipt.id,
        product1,
        AddProductRequest(id="p1", quantity=3)
    )
    receipt_service.add_product(
        receipt.id,
        product2,
        AddProductRequest(id="p2", quantity=2)
    )

    receipt_service.close_receipt(receipt.id)

    sales_data = receipt_repo.get_sales_data()
    assert sales_data is not None
    assert sales_data.n_receipts == 1
    assert sales_data.revenue == 60.0


def test_sales_data_with_currency_conversion() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    receipt_repo = sqlite.receipts()
    receipt_service = ReceiptService(receipt_repo)

    receipt = Receipt(id=str(uuid.uuid4()), status="close", products=[], total=100.0)
    receipt_repo.create(receipt)

    from app.core.constants import USD, EUR

    gel_amount = receipt_service.calculate_payment(receipt.id, "GEL")
    usd_amount = receipt_service.calculate_payment(receipt.id, USD)
    eur_amount = receipt_service.calculate_payment(receipt.id, EUR)

    assert gel_amount == 100.0

    from app.core.constants import GEL_TO_USD, GEL_TO_EUR
    assert usd_amount == round(100.0 / GEL_TO_USD, 2)
    assert eur_amount == round(100.0 / GEL_TO_EUR, 2)


def test_sales_data_across_shifts() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    shift_repo = sqlite.shifts()
    receipt_repo = sqlite.receipts()

    shift1_id = str(uuid.uuid4())
    shift2_id = str(uuid.uuid4())

    shift1 = Shift(id=shift1_id, status="close", receipts=[])
    shift2 = Shift(id=shift2_id, status="close", receipts=[])

    shift_repo.create(shift1)
    shift_repo.create(shift2)

    for shift_id in [shift1_id, shift2_id]:
        for i in range(3):
            receipt_id = str(uuid.uuid4())
            receipt = Receipt(
                id=receipt_id,
                status="close",
                products=[
                    Products(id=f"p{i}", quantity=1, price=10.0 * (i + 1), total=10.0 * (i + 1))
                ],
                total=10.0 * (i + 1)
            )
            receipt_repo.create(receipt)
            shift_repo.add_receipt_to_shift(shift_id, receipt_id)

    expected_revenue = 2 * (10.0 + 20.0 + 30.0)

    sales_data = receipt_repo.get_sales_data()
    assert sales_data is not None
    assert sales_data.n_receipts == 6
    assert sales_data.revenue == expected_revenue


def test_receipt_total_calculation() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    receipt_repo = sqlite.receipts()
    product_repo = sqlite.products()
    receipt_service = ReceiptService(receipt_repo)

    product = Product("p1", "unit", "Test Product", "1234", 25.0)
    product_repo.create(product)

    receipt = receipt_service.create()

    from app.schemas.receipt import AddProductRequest

    receipt_service.add_product(
        receipt.id,
        product,
        AddProductRequest(id="p1", quantity=2)
    )

    receipt_service.add_product(
        receipt.id,
        product,
        AddProductRequest(id="p1", quantity=3)
    )

    updated_receipt = receipt_service.read(receipt.id)

    assert updated_receipt.total == 125.0

    assert len(updated_receipt.products) == 2

    assert receipt_service.get_total(updated_receipt) == 125.0