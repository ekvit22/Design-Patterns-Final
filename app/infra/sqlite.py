import sqlite3
from dataclasses import dataclass
from typing import Optional

from app.core.Repository import Repository
from app.core.campaign.campaign import Campaign

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

@dataclass
class Sqlite:

    def campaigns(self) -> Repository[Campaign]:
        return CampaignSqliteRepository()

    def clear_tables(self) -> None:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS campaigns;")
        connection.commit()