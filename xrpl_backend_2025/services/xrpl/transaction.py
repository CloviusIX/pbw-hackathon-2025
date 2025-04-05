from typing import Any, Optional

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import XRPLReliableSubmissionException, autofill_and_sign, submit_and_wait
from xrpl.models import CheckCreate, IssuedCurrencyAmount, Memo, Payment
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


async def send_check(
    client: AsyncJsonRpcClient,
    sender_wallet: Wallet,
    destination: str,
    send_iou_max: IssuedCurrencyAmount,
    memo: Optional[Memo],
    invoice_id: Optional[str],
) -> Optional[str]:
    check_create_tx = CheckCreate(
        account=sender_wallet.classic_address,
        destination=destination,
        send_max=send_iou_max,
        memos=memo and [memo] or None,
        invoice_id=invoice_id and invoice_id or None,
    )

    signed_check = await autofill_and_sign(check_create_tx, client, sender_wallet)
    result = await submit_and_wait(signed_check, client, sender_wallet)
    return result.result.get("hash") or None
