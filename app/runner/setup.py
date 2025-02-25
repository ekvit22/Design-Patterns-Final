from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.infra.api.campaign_api import campaigns_api
from app.infra.in_memory import InMemory
from app.infra.sqlite import Sqlite


def setup() -> FastAPI:
    load_dotenv()
    api = FastAPI()

    api.state.infra = Sqlite()
    if os.getenv("REPOSITORY_KIND") == "sqlite":
        api.state.infra = Sqlite()

    api.include_router(campaigns_api, prefix="/campaigns", tags=["campaigns"])

    return api
pass
