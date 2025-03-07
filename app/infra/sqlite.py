import sqlite3
from dataclasses import dataclass
from typing import List, Optional

from app.core.campaign.campaign import Campaign
from app.core.product import Product
from app.core.receipt import Products, Receipt
from app.core.repository import ItemT, Repository
from app.core.shift import Shift
from app.schemas.sales import SalesData

connection = sqlite3.connect("database.db", check_same_thread=False)

@dataclass
class CampaignSqliteRepository:
    def __post_init__(self) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
            id TEXT,
            name TEXT,
            description TEXT
            );
            """
        )
        # connection.execute("""DROP TABLE campaigns;""")
        connection.commit()


    def create(self, item: Campaign) -> Campaign:
        connection.execute(
            """
            Insert into campaigns(id, name, description)
             values (?, ?, ?)
            """,
            (item.id, item.name, item.description),
        )
        connection.commit()
        return item

    def read(self, item_id: str) -> Optional[Campaign]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM campaigns WHERE id = ?", (item_id,))

        row = cursor.fetchone()
        if row is None:
            return None

        return Campaign(row[0], row[1], row[2])


    def read_with_name(self, item_name: str) -> Optional[Campaign]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM campaigns WHERE name = ?", (item_name,))

        row = cursor.fetchone()
        if row is None:
            return None

        return Campaign(row[0], row[1], row[2])

    def update(self, item: Campaign) -> None:
        return None


    def delete(self, item_id: str) -> None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM campaigns WHERE id = ?", (item_id,))
        connection.commit()

    def get_all(self) -> list[Campaign]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM campaigns")
        res: list[Campaign] = []
        for row in cursor.fetchall():
            res.append(Campaign(row[0], row[1], row[2]))
        return res

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        return

    def close_receipt(self, receipt_id: str) -> None:
        return

    def open_shift(self, receipt_id: str) -> None:
        return

    def open_receipt(self, receipt_id: str) -> None:
        return

    def close_shift(self, shift_id: str) -> None:
        return

    def read_with_barcode(self, item_barcode: str) -> Optional[ItemT]:
        return None

    def get_every_receipt(self, receipt_ids: List[str]) -> List[ItemT]:
        return []

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        return []

    def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
        return []

    def get_sales_data(self) -> Optional[SalesData]:
        return None

@dataclass
class ReceiptRepository(Repository[Receipt]):
    def __post_init__(self) -> None:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id TEXT,
                status TEXT,
                total REAL
            );
        """)
        connection.commit()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS receipts_products (
                product_id TEXT,
                receipt_id TEXT,
                quantity INTEGER,
                price REAL,
                total REAL,
                FOREIGN KEY (receipt_id) REFERENCES receipts(receipt_id)
            );
        """)

        connection.commit()

    def create(self, item: Receipt) -> Receipt:
        connection.execute("""
            INSERT INTO receipts(receipt_id, status, total)
            VALUES(?, ?, ?)""",
            (item.id, item.status, item.total)
        )

        for product in item.products:
            connection.execute("""
                INSERT INTO receipts_products(product_id, receipt_id,
                 quantity, price, total)
                VALUES(?, ?, ?, ?, ?)""",
                (product.id, item.id, product.quantity, product.price, product.total)
            )
        connection.commit()
        return item


    def add_product(self, receipt_id: str, product: Products) -> None:
        connection.execute("""
            INSERT INTO receipts_products(product_id, receipt_id,
             quantity, price, total)
            VALUES(?, ?, ?, ?, ?)""",
            (product.id, receipt_id, product.quantity, product.price, product.total)
        )

        connection.execute("""
            UPDATE receipts SET total = total + ? WHERE receipt_id = ?""",
           (product.total, receipt_id)
        )
        connection.commit()

    def open_receipt(self, receipt_id: str) -> None:
        connection.execute("""
            UPDATE receipts SET status = ? WHERE receipt_id = ?""",
            ("open", receipt_id)
        )
        connection.commit()

    def close_receipt(self, receipt_id: str) -> None:
        connection.execute("""
            UPDATE receipts SET status = ? WHERE receipt_id = ?""",
            ("close", receipt_id)
        )
        connection.commit()

    def update(self, item: Receipt) -> None:
        self.delete(item.id)
        self.create(item)

    def delete(self, item_id: str) -> None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM receipts WHERE receipt_id = ?", (item_id,))
        cursor.execute("DELETE FROM receipt_products WHERE receipt_id = ?", (item_id,))
        connection.commit()

    def get_every_receipt(self, receipt_ids: List[str]) -> List[Receipt]:
        cursor = connection.cursor()
        receipts = []
        for receipt_id in receipt_ids:
            cursor.execute("SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,))
            receipt_row = cursor.fetchone()
            if receipt_row is not None:
                products = self.get_products_from_receipt(receipt_row[0])
                receipts.append(Receipt(id=receipt_row[0], status=receipt_row[1],
                                        products=products, total=receipt_row[2]))
        return receipts

    def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM receipts_products WHERE receipt_id = ?""",
                       (receipt_id,))
        product_rows = cursor.fetchall()
        products = [Products(id=product_row[0], quantity=product_row[2],
                             price=product_row[3], total=product_row[4])
                    for product_row in product_rows]
        return products

    def read(self, receipt_id: str) -> Optional[Receipt]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,))
        receipt_row = cursor.fetchone()
        if receipt_row is  None:
            return None
        products = self.get_products_from_receipt(receipt_id)
        result = Receipt(id=receipt_row[0], status=receipt_row[1], products=products,
                         total=receipt_row[2])
        return result

    def get_sales_data(self) -> Optional[SalesData]:
        res: SalesData = SalesData(n_receipts=0, revenue=0)
        cursor = connection.cursor()
        cursor.execute("SELECT total FROM receipts", )
        for row in cursor.fetchall():
            res.n_receipts += 1
            res.revenue += row[0]

        return res

    def read_with_name(self, item_name: str) -> Optional[Receipt]:
        return None

    def read_with_barcode(self, barcode: str) -> Optional[Receipt]:
        return None

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        return None

    def open_shift(self, shift_id: str) -> None:
        return None

    def close_shift(self, shift_id: str) -> None:
        return None

    def get_all(self) -> List[Receipt]:
        return []

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        return []

@dataclass
class ShiftRepository(Repository[Shift]):
    def __post_init__(self) -> None:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                shift_id TEXT,
                status TEXT
            )
        """)
        connection.commit()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS shift_receipts (
                shift_id TEXT,
                receipt_id TEXT,
                FOREIGN KEY (shift_id) REFERENCES shifts (shift_id)
            )
        """)
        connection.commit()

    def create(self, item: Shift) -> Shift:
        connection.execute("""
            INSERT INTO shifts(shift_id, status)
            VALUES(?, ?)""",
            (item.id, item.status)
        )
        connection.commit()
        return item

    def read(self, shift_id: str) -> Optional[Shift]:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM shifts WHERE shift_id = ?""", (shift_id,))
        shift_row = cursor.fetchone()
        if shift_row is None:
            return None
        receipts = self.get_shift_receipt_ids(shift_id)
        return Shift(id=shift_row[0], status=shift_row[1], receipts=receipts)

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM shift_receipts WHERE shift_id = ?""",
                       (shift_id,))
        return [row[1] for row in cursor.fetchall()]

    def open_shift(self, shift_id: str) -> None:
        connection.execute("""
            UPDATE shifts SET status = ? WHERE shift_id = ?""",
            ("open", shift_id)
        )
        connection.commit()

    def close_shift(self, shift_id : str) -> None:
        connection.execute("""
            UPDATE shifts SET status = ? WHERE shift_id = ?""",
            ("close", shift_id)
        )
        connection.commit()

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        connection.execute("""
            INSERT INTO shift_receipts(shift_id, receipt_id)
            VALUES(?, ?)""",
            (shift_id, receipt_id)
        )
        connection.commit()

    def get_sales_data(self) -> Optional[SalesData]:
        return None

    def update(self, item: Shift) -> None:
        connection.execute("""
            UPDATE shifts SET status = ? WHERE shift_id = ?""",
                           (item.status, item.id)
                           )
        connection.commit()

    def delete(self, item_id: str) -> None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM shifts WHERE shift_id = ?", (item_id,))
        cursor.execute("DELETE FROM shift_receipts WHERE shift_id = ?", (item_id,))
        connection.commit()

    def close_receipt(self, receipt_id: str) -> None:
        return None

    def open_receipt(self, receipt_id: str) -> None:
        return None

    def read_with_name(self, item_name: str) -> Optional[Shift]:
        return None

    def read_with_barcode(self, item_barcode: str) -> Optional[Shift]:
        return None

    def get_every_receipt(self, receipt_ids: List[str]) -> List[Shift]:
        return []

    def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
        return []

    def get_all(self) -> List[Shift]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shifts")
        shifts = []
        for shift_row in cursor.fetchall():
            shift_id = shift_row[0]
            receipts = self.get_shift_receipt_ids(shift_id)
            shifts.append(Shift(id=shift_id, status=shift_row[1], receipts=receipts))
        return shifts

@dataclass
class ProductSqliteRepository(Repository[Product]):

    def __post_init__(self) -> None:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT,
                unit TEXT,
                name TEXT,
                barcode TEXT,
                price REAL
            );
            """
        )
        connection.commit()


    def create(self, item: Product) -> Product:
        connection.execute(
            """
            Insert into products(id, unit, name, barcode, price)
             values (?, ?, ?, ?, ?)
            """,
            (item.id, item.unit, item.name, item.barcode, item.price),
        )
        connection.commit()
        return item

    def read(self, item_id: str) -> Optional[Product]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if row is not None:
            return Product(row[0], row[1], row[2], row[3], row[4])
        return None


    def read_with_name(self, item_name: str) -> Optional[Product]:
        return None

    def read_with_barcode(self, item_barcode: str) -> Optional[Product]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode = ?", (item_barcode,))
        row = cursor.fetchone()
        if row is not None:
            return Product(row[0], row[1], row[2], row[3], row[4])
        return None

    def update(self, item: Product) -> None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (item.id,))

        connection.execute(
            """
            Insert into products(id, unit, name, barcode, price)
             values (?, ?, ?, ?, ?)
            """,
            (item.id, item.unit, item.name, item.barcode, item.price),
        )

        connection.commit()


    def get_all(self) -> List[Product]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        res: List[Product] = []
        for row in cursor.fetchall():
            res.append(Product(row[0], row[1], row[2], row[3], row[4]))
        return res


    def delete(self, item_id: str) -> None:
        return None

    def get_sales_data(self) -> Optional[SalesData]:
        return None

    def open_receipt(self, receipt_id: str) -> None:
        return None

    def close_receipt(self, receipt_id: str) -> None:
        return None

    def get_every_receipt(self, receipt_ids: List[str]) -> List[Product]:
        return []

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        return []

    def open_shift(self, shift_id: str) -> None:
        return None

    def close_shift(self, shift_id: str) -> None:
        return None

    def add_receipt_to_shift(self, shift_id: str, receipt_id: str) -> None:
        return None

    def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
        return []

@dataclass
class Sqlite:

    def campaigns(self) -> Repository[Campaign]:
        return CampaignSqliteRepository()

    def receipts(self) -> Repository[Receipt]:
        return ReceiptRepository()

    def shifts(self) -> Repository[Shift]:
        return ShiftRepository()

    def products(self) -> Repository[Product]:
        return ProductSqliteRepository()

    def clear_tables(self) -> None:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS campaigns;")
        cursor.execute("DROP TABLE IF EXISTS receipts;")
        cursor.execute("DROP TABLE IF EXISTS receipts_products;")
        cursor.execute("DROP TABLE IF EXISTS shifts;")
        cursor.execute("DROP TABLE IF EXISTS shift_receipts;")
        cursor.execute("DROP TABLE IF EXISTS products;")

        connection.commit()