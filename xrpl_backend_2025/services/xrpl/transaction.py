from typing import Any

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import XRPLReliableSubmissionException, autofill_and_sign, submit_and_wait
from xrpl.models import IssuedCurrencyAmount, Payment
from xrpl.wallet import Wallet


async def send_payment(
    client: AsyncJsonRpcClient,
    wallet: Wallet,
    amount_to_send: str | IssuedCurrencyAmount,
    destination: str,
) -> dict[str, Any] | None:
    payment = Payment(account=wallet.address, amount=amount_to_send, destination=destination)
    signed_tx = await autofill_and_sign(payment, client, wallet)
    # TODO ? It's also a good idea to take note of the latest validated ledger index before you submit.
    try:
        tx = await submit_and_wait(signed_tx, client, wallet)
    except XRPLReliableSubmissionException as e:
        print(f"Failed to submit payment: {e}")
        return None

    return tx.result
