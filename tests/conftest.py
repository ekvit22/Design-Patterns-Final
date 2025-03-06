from typing import Generator

import pytest
from starlette.testclient import TestClient

from app.infra.sqlite import Sqlite
from app.runner.setup import setup


@pytest.fixture # type: ignore
def http() -> TestClient:
    return TestClient(setup())

@pytest.fixture(autouse=True) # type: ignore
def clean_database() -> Generator[None, None, None]:
    sqlite: Sqlite = Sqlite()
    sqlite.clear_tables()
    yield
    sqlite = Sqlite()
    sqlite.clear_tables()