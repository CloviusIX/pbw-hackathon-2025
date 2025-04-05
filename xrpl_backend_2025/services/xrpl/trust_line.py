from typing import Any

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import (
    XRPLReliableSubmissionException,
    autofill_and_sign,
    submit_and_wait,
)
from xrpl.models import IssuedCurrencyAmount, TrustSet
from xrpl.wallet import Wallet


async def set_trustline(
    client: AsyncJsonRpcClient,
    recipient_wallet: Wallet,
    icm: IssuedCurrencyAmount,
) -> dict[str, Any] | None:
    trustline_tx = TrustSet(account=recipient_wallet.classic_address, limit_amount=icm)
    signed_tx = await autofill_and_sign(trustline_tx, client, recipient_wallet)
    try:
        response = await submit_and_wait(signed_tx, client, recipient_wallet)
    except XRPLReliableSubmissionException as e:
        raise Exception(f"Failed to submit payment: {e}")

    return response.result
