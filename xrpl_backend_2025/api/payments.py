from fastapi import APIRouter, HTTPException
from pydantic_settings import BaseSettings
from xrpl import CryptoAlgorithm
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models import IssuedCurrencyAmount
from xrpl.utils import xrp_to_drops
from xrpl.wallet import Wallet

from xrpl_backend_2025.constants.xrpl_constants import RLUSD_CURRENCY, RLUSD_ISSUER
from xrpl_backend_2025.schemas.payments import CheckRequest, CheckResponse, PaymentRequest, PaymentResponse
from xrpl_backend_2025.services.xrpl.accounts import get_account_info, get_account_objects, get_check_id
from xrpl_backend_2025.services.xrpl.transaction import send_check, send_payment
from xrpl_backend_2025.utils.xrpl_utils import to_hex_memo, to_invoice_id

router = APIRouter()


class Settings(BaseSettings):
    xrpl_node: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
RPC_NODE = settings.xrpl_node


@router.post("/")
async def create_payment(payment: PaymentRequest) -> PaymentResponse:
    try:
        client = AsyncJsonRpcClient(RPC_NODE)
        wallet = Wallet.from_seed(seed=payment.seed, algorithm=CryptoAlgorithm.ED25519)

        tx = await send_payment(client, wallet, xrp_to_drops(payment.amount), payment.destination)
        account_info = await get_account_info(client=client, wallet_address=wallet.address)
        new_native_balance = account_info.account_data.balance
        tx_hash = tx and tx.get("hash") or ""
        return PaymentResponse(hash=tx_hash, balance=int(new_native_balance))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checks")
async def create_check(check: CheckRequest) -> CheckResponse:
    client = AsyncJsonRpcClient(RPC_NODE)
    wallet = Wallet.from_seed(seed=check.seed, algorithm=CryptoAlgorithm.ED25519)
    icm = IssuedCurrencyAmount(value=check.amount, currency=RLUSD_CURRENCY, issuer=RLUSD_ISSUER)

    memo = check.memo and to_hex_memo(check.memo) or None
    invoice_id = check.invoice_id and to_invoice_id(check.invoice_id) or None

    check_hash = await send_check(
        client=client,
        sender_wallet=wallet,
        destination=check.destination,
        send_iou_max=icm,
        memo=memo,
        invoice_id=invoice_id,
    )

    account_objects = await get_account_objects(client, check.destination)
    check_id = await get_check_id(account_objects)
    return CheckResponse(check_hash=check_hash, check_id=check_id)
