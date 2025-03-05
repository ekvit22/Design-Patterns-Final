from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI

from app.infra.api.campaign_api import campaigns_api
from app.infra.api.products import products_api
from app.infra.api.receipt_api import receipt_api
from app.infra.api.sales import sales_api
from app.infra.api.shift_api import shift_api
from app.infra.api.xreport import xreport_api
from app.infra.in_memory import InMemory


def setup() -> FastAPI:
    load_dotenv()
    api = FastAPI()

    api.state.infra = InMemory()
    # if os.getenv("REPOSITORY_KIND") == "sqlite":
    #     api.state.infra = Sqlite()

    api.include_router(products_api, prefix="/products", tags=["products"])
    api.include_router(campaigns_api, prefix="/campaigns", tags=["campaigns"])
    api.include_router(receipt_api, prefix="/receipts", tags=["receipts"])
    api.include_router(shift_api, prefix="/shifts", tags=["shifts"])
    api.include_router(xreport_api, prefix="/xreports", tags=["xreports"])
    api.include_router(sales_api, prefix="/sales", tags=["sales"])

    return api
pass
