from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic_settings import BaseSettings
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.wallet import Wallet

from xrpl_backend_2025.constants.xrpl_constants import RLUSD_CURRENCY, RLUSD_ISSUER
from xrpl_backend_2025.schemas.balances import BalanceRequest
from xrpl_backend_2025.services.xrpl.accounts import get_account_info, get_iou_balance, get_xrp_balance

router = APIRouter()


class Settings(BaseSettings):
    xrpl_node: str = ""

    class Config:
        env_file = ".env"


async def get_xrpl_client() -> AsyncJsonRpcClient:
    return AsyncJsonRpcClient(settings.xrpl_node)


settings = Settings()


@router.post("/")
async def get_xrp_balances(
    balance_req: BalanceRequest, client: AsyncJsonRpcClient = Depends(get_xrpl_client)
) -> Decimal:
    try:
        wallet = Wallet.from_seed(seed=balance_req.seed)
        account_info = await get_account_info(client=client, wallet_address=wallet.address)
        balance = await get_xrp_balance(account_info)
        return balance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ious")
async def get_iou_balances(
    balance_req: BalanceRequest, client: AsyncJsonRpcClient = Depends(get_xrpl_client)
) -> Decimal:
    try:
        wallet = Wallet.from_seed(seed=balance_req.seed)
        # For presentation purposes, getting $RLUSD
        balance = await get_iou_balance(
            client=client, wallet_address=wallet.classic_address, iou_issuer=RLUSD_ISSUER, iou_currency=RLUSD_CURRENCY
        )
        return balance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
