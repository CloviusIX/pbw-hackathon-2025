from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic_settings import BaseSettings
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.wallet import Wallet

from xrpl_backend_2025.schemas.balances import BalanceRequest
from xrpl_backend_2025.services.xrpl.accounts import get_account_info, get_xrp_balance

router = APIRouter()


class Settings(BaseSettings):
    xrpl_node: str = ""

    class Config:
        env_file = ".env"


async def get_xrpl_client() -> AsyncJsonRpcClient:
    return AsyncJsonRpcClient(settings.xrpl_node)


settings = Settings()


@router.post("/")
async def create_native_payment(
    balance_req: BalanceRequest, client: AsyncJsonRpcClient = Depends(get_xrpl_client)
) -> Decimal:
    try:
        wallet = Wallet.from_seed(seed=balance_req.seed)
        account_info = await get_account_info(client=client, wallet_address=wallet.address)
        balance = await get_xrp_balance(account_info)
        return balance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
