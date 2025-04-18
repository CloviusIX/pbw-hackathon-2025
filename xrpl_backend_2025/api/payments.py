from fastapi import APIRouter, Depends, HTTPException
from pydantic_settings import BaseSettings
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models import IssuedCurrencyAmount
from xrpl.utils import xrp_to_drops
from xrpl.wallet import Wallet

from xrpl_backend_2025.constants.xrpl_constants import RLUSD_CURRENCY, RLUSD_ISSUER, RLUSD_PATH_STEP
from xrpl_backend_2025.schemas.payments import (
    CheckRequest,
    CheckResponse,
    CrossPaymentRequest,
    PaymentRequest,
    PaymentResponse,
)
from xrpl_backend_2025.services.xrpl.accounts import (
    get_account_info,
    get_account_objects,
    get_check_id,
    get_xrp_balance,
)
from xrpl_backend_2025.services.xrpl.transaction import send_check, send_payment, swap_xrp_for_token
from xrpl_backend_2025.services.xrpl.trust_line import set_trustline
from xrpl_backend_2025.utils.xrpl_utils import to_hex_memo, to_invoice_id

router = APIRouter()


class Settings(BaseSettings):
    xrpl_node: str = ""

    class Config:
        env_file = ".env"


settings = Settings()


async def get_xrpl_client() -> AsyncJsonRpcClient:
    return AsyncJsonRpcClient(settings.xrpl_node)


@router.post("/")
async def create_native_payment(
    payment: PaymentRequest, client: AsyncJsonRpcClient = Depends(get_xrpl_client)
) -> PaymentResponse:
    try:
        wallet = Wallet.from_seed(seed=payment.seed)
        memo = payment.memo and to_hex_memo(payment.memo) or None

        tx_hash = await send_payment(
            client=client,
            wallet=wallet,
            amount_to_send=xrp_to_drops(payment.amount),
            destination=payment.destination,
            memo=memo,
        )
        account_info = await get_account_info(client=client, wallet_address=wallet.address)
        new_native_balance = await get_xrp_balance(account_info)
        return PaymentResponse(hash=tx_hash, balance=new_native_balance)
    except Exception as e:
        # TODO: manage UNFUNDED_PAYMENT
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cross")
async def create_cross_payment(
    payment: CrossPaymentRequest, client: AsyncJsonRpcClient = Depends(get_xrpl_client)
) -> PaymentResponse:
    try:
        wallet = Wallet.from_seed(seed=payment.seed)

        # set trust line to iou
        # TODO: check if trust line already exist ?
        icm = IssuedCurrencyAmount(value=payment.iou_amount, currency=payment.iou_currency, issuer=payment.iou_issuer)
        await set_trustline(client, wallet, icm)

        # workaround to get issuer path step
        # assuming we swap for $RLUSD
        token_to_swap_for = RLUSD_PATH_STEP

        tx_hash = await swap_xrp_for_token(
            client=client,
            sender_wallet=wallet,
            destination=payment.destination,
            token_to_swap_for=token_to_swap_for,  # PathStep(currency, issuer)
            iou_amount=payment.iou_amount,
            max_xrp_to_send=xrp_to_drops(payment.xrp_amount),
        )

        account_info = await get_account_info(client=client, wallet_address=wallet.address)
        new_native_balance = await get_xrp_balance(account_info)
        return PaymentResponse(hash=tx_hash, balance=new_native_balance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checks")
async def create_check(check: CheckRequest, client: AsyncJsonRpcClient = Depends(get_xrpl_client)) -> CheckResponse:
    wallet = Wallet.from_seed(seed=check.seed)

    # using $RLUSD by default for presentation and avoid price volatility
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
