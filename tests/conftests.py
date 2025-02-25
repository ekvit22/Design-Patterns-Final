from pathlib import Path
from typing import Generator

import pytest
from starlette.testclient import TestClient

from app.infra.sqlite import Sqlite
from app.runner.setup import setup

file_path = Path("database.db")

@pytest.fixture
def http() -> TestClient:
    return TestClient(setup())

@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
    sqlite: Sqlite = Sqlite()
    sqlite.clear_tables()
    yield
    sqlite = Sqlite()
    sqlite.clear_tables()