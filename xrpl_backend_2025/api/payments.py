
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from xrpl import CryptoAlgorithm
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.utils import xrp_to_drops
from xrpl.wallet import Wallet

from xrpl_backend_2025.services.xrpl.accounts import get_account_info
from xrpl_backend_2025.services.xrpl.transaction import send_payment

router = APIRouter()


class Settings(BaseSettings):
    xrpl_node: str = "default_value"

    class Config:
        env_file = ".env"


settings = Settings()


class PaymentRequest(BaseModel):
    amount: int
    destination: str
    seed: str


class PaymentResponse(BaseModel):
    hash: str
    balance: int


@router.post("/")
async def create_payment(payment: PaymentRequest) -> PaymentResponse:
    try:
        rpc_node = settings.xrpl_node
        client = AsyncJsonRpcClient(rpc_node)
        wallet = Wallet.from_seed(seed=payment.seed, algorithm=CryptoAlgorithm.ED25519)

        tx = await send_payment(client, wallet, xrp_to_drops(payment.amount), payment.destination)
        account_info = await get_account_info(client=client, wallet_address=wallet.address)
        new_native_balance = account_info.account_data.balance
        tx_hash = tx and tx.get("hash") or ""
        return PaymentResponse(hash=tx_hash, balance=int(new_native_balance))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
