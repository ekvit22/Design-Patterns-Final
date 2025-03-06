from app.core.repository import Repository
from app.core.campaign.campaign import Campaign
from app.infra.sqlite import Sqlite
from app.core.receipt import Receipt, Products
from app.core.shift import Shift
from app.core.xreport import XReport



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
    sqlite = Sqlite()
    sqlite.clear_tables()

    shifts: Repository[Shift] = sqlite.shifts()
    receipts: Repository[Receipt] = sqlite.receipts()
    products: Repository[Product] = sqlite.products()
    xreports: Repository[XReport] = sqlite.xreport()

    shift = Shift("shift123", "open", [])
    shifts.create(shift)

    products.create(Product("p1", "unit1", "apple", "1111", 10))
    products.create(Product("p2", "unit2", "banana", "2222", 15))

    receipt1 = Receipt(
        id="r1",
        status="close",
        products=[
            Products(id="p1", quantity=2, price=10, total=20),
            Products(id="p2", quantity=1, price=15, total=15)
        ],
        total=35
    )

    receipt2 = Receipt(
        id="r2",
        status="close",
        products=[
            Products(id="p1", quantity=1, price=10, total=10),
            Products(id="p2", quantity=3, price=15, total=45)
        ],
        total=55
    )

    receipts.create(receipt1)
    receipts.create(receipt2)

    shift_repo = sqlite.shifts()
    shift_repo.add_receipt_to_shift("shift123", "r1")
    shift_repo.add_receipt_to_shift("shift123", "r2")

    xreport = xreports.generate_x_report("shift123", shift, receipts)

    assert xreport is not None
    assert xreport.shift_id == "shift123"
    assert xreport.total_receipts == 2
    assert xreport.revenue == 90.0

    # Check items sold
    assert "p1" in xreport.items_sold
    assert "p2" in xreport.items_sold
    assert xreport.items_sold["p1"] == 3
    assert xreport.items_sold["p2"] == 4


def test_xreport_empty_shift() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    shifts: Repository[Shift] = sqlite.shifts()
    receipts: Repository[Receipt] = sqlite.receipts()
    xreports: Repository[XReport] = sqlite.xreport()

    empty_shift = Shift("empty123", "open", [])
    shifts.create(empty_shift)

    xreport = xreports.generate_x_report("empty123", empty_shift, receipts)

    assert xreport is None


def test_xreport_with_multiple_products() -> None:
    sqlite = Sqlite()
    sqlite.clear_tables()

    shifts: Repository[Shift] = sqlite.shifts()
    receipts: Repository[Receipt] = sqlite.receipts()
    products: Repository[Product] = sqlite.products()
    xreports: Repository[XReport] = sqlite.xreport()

    products.create(Product("p1", "unit1", "apple", "1111", 10))
    products.create(Product("p2", "unit2", "banana", "2222", 15))
    products.create(Product("p3", "unit3", "orange", "3333", 12))

    shift = Shift("complex123", "open", [])
    shifts.create(shift)

    receipt1 = Receipt(
        id="r1",
        status="close",
        products=[
            Products(id="p1", quantity=2, price=10, total=20),
            Products(id="p2", quantity=1, price=15, total=15),
            Products(id="p3", quantity=3, price=12, total=36)
        ],
        total=71
    )

    receipt2 = Receipt(
        id="r2",
        status="close",
        products=[
            Products(id="p1", quantity=1, price=10, total=10),
            Products(id="p3", quantity=2, price=12, total=24)
        ],
        total=34
    )

    receipt3 = Receipt(
        id="r3",
        status="close",
        products=[
            Products(id="p2", quantity=4, price=15, total=60)
        ],
        total=60
    )

    receipts.create(receipt1)
    receipts.create(receipt2)
    receipts.create(receipt3)

    shift_repo = sqlite.shifts()
    shift_repo.add_receipt_to_shift("complex123", "r1")
    shift_repo.add_receipt_to_shift("complex123", "r2")
    shift_repo.add_receipt_to_shift("complex123", "r3")

    xreport = xreports.generate_x_report("complex123", shift, receipts)

    assert xreport is not None
    assert xreport.shift_id == "complex123"
    assert xreport.total_receipts == 3
    assert xreport.revenue == 165.0

    # Check items sold
    assert xreport.items_sold["p1"] == 3
    assert xreport.items_sold["p2"] == 5
    assert xreport.items_sold["p3"] == 5