import sqlite3
from dataclasses import dataclass
from typing import Optional

from app.core.Repository import Repository
from app.core.campaign import Campaign

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
        # connection.commit()


    def create(self, item: Campaign) -> Campaign:
        connection.execute(
            """
            Insert into campaigns(id, name, discount_type, product_id, products, discount, gift_id, gift_required_count)
             values (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (item.id, item.name, item.type, item.product_id, ";".join(item.products), item.discount, item.gift_id, item.gift_required_count),
        )
        # connection.commit()
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
        # connection.commit()

    def get_all(self) -> list[Campaign]:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM campaigns")
        res: list[Campaign] = []
        for row in cursor.fetchall():
            res.append(Campaign(row[0], row[1], row[2], row[3], row[4].split(";"), row[5], row[6], row[7]))
        return res

@dataclass
class Sqlite:

    def campaigns(self) -> Repository[Campaign]:
        return CampaignSqliteRepository()

    def clear_tables(self) -> None:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS campaigns;")
        connection.commit()