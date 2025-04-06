from fastapi import FastAPI

from xrpl_backend_2025.api import balances, payments


def include_routes(app: FastAPI) -> None:
    app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
    app.include_router(balances.router, prefix="/api/balances", tags=["Balances"])
