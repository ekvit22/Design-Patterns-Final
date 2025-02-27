import sqlite3
from dataclasses import dataclass
from typing import Optional, List

from app.core.receipt import Receipt, Products
from app.core.repository import Repository
from app.core.campaign import Campaign
from app.core.shift import Shift

connection = sqlite3.connect("database.db", check_same_thread=False)

@dataclass
class CampaignSqliteRepository:
    def __post_init__(self) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
            id TEXT,
            name TEXT,
            discount_type TEXT,
            product_id TEXT,
            products TEXT,
            discount int,
            gift_id TEXT,
            gift_required_count int
            );
            """
        )
        # connection.execute("""DROP TABLE campaigns;""")
        connection.commit()


    def create(self, item: Campaign) -> Campaign:
        connection.execute(
            """
            Insert into campaigns(id, name, discount_type, product_id, products, discount, gift_id, gift_required_count)
             values (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (item.id, item.name, item.type, item.product_id, ";".join(item.products), item.discount, item.gift_id, item.gift_required_count),
        )
        connection.commit()
        return item

    def read(self, item_id: str) -> Optional[Campaign]:
        return None


    def read_with_name(self, item_name: str) -> Optional[Campaign]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM campaigns WHERE name = ?", (item_name,))

        row = cursor.fetchone()
        if row is None:
            return None

        return Campaign(row[0], row[1], row[2], row[3], row[4].split(";"), row[5], row[6], row[7])

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
            res.append(Campaign(row[0], row[1], row[2], row[3], row[4].split(";"), row[5], row[6], row[7]))
        return res

@dataclass
class ReceiptRepository:
    def __post_init__(self) -> None:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id TEXT,
                status TEXT,
                total INTEGER,
            )
        """)
        # connection.commit()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS receipts_products (
                product_id TEXT,
                receipt_id TEXT,
                quantity INTEGER,
                price INTEGER,
                total INTEGER,
                FOREIGN KEY (receipt_id) REFERENCES receipts(receipt_id)
            )
        """)

        # connection.commit()

    def create(self, item: Receipt) -> None:
        connection.execute("""
            INSERT INTO receipts(receipt_id, status, total)
            VALUES(?, ?, ?)""",
            (item.receipt_id, item.status, item.total)
        )

        for product in item.products:
            connection.execute("""
                INSERT INTO receipts_products(product_id, receipt_id, quantity, price, total)
                VALUES(?, ?, ?, ?, ?)""",
                (product.product_id, item.receipt_id, product.quantity, product.price, product.total)
            )
        # connection.commit()


    def add_product(self, receipt_id: str, product: Products) -> None:
        connection.execute("""
            INSERT INTO receipts_products(product_id, receipt_id, quantity, price, total)
            VALUES(?, ?, ?, ?, ?)""",
            (product.product_id, receipt_id, product.quantity, product.price, product.total)
        )

        connection.execute("""
            UPDATE receipts SET total = total + ? WHERE receipt_id = ?""",
           (product.total, receipt_id)
        )
        # connection.commit()
    #
    def open_receipt(self, receipt_id: str) -> None:
        connection.execute("""
            UPDATE receipts SET status = ? WHERE receipt_id = ?""",
            ("open", receipt_id)
        )
        # connection.commit()

    def close_receipt(self, receipt_id: str) -> None:
        connection.execute("""
            UPDATE receipts SET status = ? WHERE receipt_id = ?""",
            ("close", receipt_id)
        )
        # connection.commit()

    def update(self, item: Receipt) -> None:
        self.delete(item.receipt_id)
        self.create(item)

    def delete(self, item_id: str) -> None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM receipts WHERE receipt_id = ?", (item_id,))
        cursor.execute("DELETE FROM receipt_products WHERE receipt_id = ?", (item_id,))
        connection.commit()

    def get_all(self) -> List[Receipt]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM receipts")
        receipts = []
        for receipt_row in cursor.fetchall():
            products = self.get_products_from_receipt(receipt_row[0])
            receipts.append(Receipt(receipt_id=receipt_row[0], status=receipt_row[1], products=products, total=receipt_row[2]))
        return receipts

    def get_every_receipt(self, receipt_ids: List[str]) -> List[Receipt]:
        cursor = connection.cursor()
        receipts = []
        for receipt_id in receipt_ids:
            cursor.execute("SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,))
            receipt_row = cursor.fetchone()
            if receipt_row is not None:
                products = self.get_products_from_receipt(receipt_row[0])
                receipts.append(Receipt(receipt_id=receipt_row[0], status=receipt_row[1], products=products, total=receipt_row[2]))
        return receipts

    def get_products_from_receipt(self, receipt_id: str) -> List[Products]:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM receipts_products WHERE receipt_id = ?""", (receipt_id,))
        product_rows = cursor.fetchall()
        products = [Products(product_id=product_row[0], quantity=product_row[2], price=product_row[3], total=product_row[4]) for product_row in product_rows]
        return products

    def read(self, receipt_id: str) -> Optional[Receipt]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,))
        receipt_row = cursor.fetchone()
        if receipt_row is  None:
            return None
        products = self.get_products_from_receipt(receipt_id)
        result = Receipt(receipt_id=receipt_row[0], status=receipt_row[1], products=products, total=receipt_row[2])
        return result

@dataclass
class ShiftRepository(Repository[Shift]):
    def __post_init__(self) -> None:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                shift_id TEXT,
                status TEXT
            )
        """)
        # connection.commit()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS shift_receipts (
                shift_id TEXT,
                receipt_id TEXT,
                FOREIGN KEY (shift_id) REFERENCES shifts (shift_id)
            )
        """)
        # connection.commit()

    def create(self, request: Shift) -> None:
        connection.execute("""
            INSERT INTO shifts(shift_id, status)
            VALUES(?, ?)""",
            (request.shift_id, request.status)
        )
        # connection.commit()

    def get_shift_receipt_ids(self, shift_id: str) -> List[str]:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM shift_receipts WHERE shift_id = ?""", (shift_id,))
        return [row[0] for row in cursor.fetchall()]

    def open_shift(self, shift_id: str) -> None:
        connection.execute("""
            UPDATE shifts SET status = ? WHERE shift_id = ?""",
            ("open", shift_id)
        )
        # connection.commit()

    def close_shift(self, shift_id : str) -> None:
        connection.execute("""
            UPDATE shifts SET status = ? WHERE shift_id = ?""",
            ("close", shift_id)
        )
        # connection.commit()


@dataclass
class Sqlite:

    def campaigns(self) -> Repository[Campaign]:
        return CampaignSqliteRepository()

    def receipts(self) -> Repository[Receipt]:
        return ReceiptRepository()



    def clear_tables(self) -> None:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS campaigns;")
        cursor.execute("DROP TABLE IF EXISTS receipts;")
        cursor.execute("DROP TABLE IF EXISTS receipts_products;")
        cursor.execute("DROP TABLE IF EXISTS shifts;")
        cursor.execute("DROP TABLE IF EXISTS shift_receipts;")

        connection.commit()