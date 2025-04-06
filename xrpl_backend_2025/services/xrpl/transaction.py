from typing import Optional

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import XRPLReliableSubmissionException, autofill_and_sign, submit_and_wait
from xrpl.models import CheckCreate, IssuedCurrencyAmount, Memo, PathStep, Payment
from xrpl.wallet import Wallet

from xrpl_backend_2025.models.transaction import TransactionData


async def send_payment(
    client: AsyncJsonRpcClient,
    wallet: Wallet,
    amount_to_send: str | IssuedCurrencyAmount,
    destination: str,
    memo: Optional[Memo],
) -> str:
    memos = memo and [memo] or None
    payment = Payment(account=wallet.address, amount=amount_to_send, destination=destination, memos=memos)
    signed_tx = await autofill_and_sign(payment, client, wallet)
    try:
        tx = await submit_and_wait(signed_tx, client, wallet)
    except XRPLReliableSubmissionException as e:
        raise Exception(f"Failed to submit payment: {e}")

    tx_data = TransactionData.model_validate(tx.result)
    return tx_data.hash


async def send_check(
    client: AsyncJsonRpcClient,
    sender_wallet: Wallet,
    destination: str,
    send_iou_max: IssuedCurrencyAmount,
    memo: Optional[Memo],
    invoice_id: Optional[str],
) -> str:
    check_create_tx = CheckCreate(
        account=sender_wallet.classic_address,
        destination=destination,
        send_max=send_iou_max,
        memos=memo and [memo] or None,
        invoice_id=invoice_id and invoice_id or None,
    )

    signed_check = await autofill_and_sign(check_create_tx, client, sender_wallet)
    try:
        tx = await submit_and_wait(signed_check, client, sender_wallet)
    except XRPLReliableSubmissionException as e:
        raise Exception(f"Failed to send check: {e}")

    tx_data = TransactionData.model_validate(tx.result)
    return tx_data.hash


async def swap_xrp_for_token(
    client: AsyncJsonRpcClient,
    sender_wallet: Wallet,
    destination: str,
    token_to_swap_for: PathStep,  # IOU (e.g., RLUSD) in hex format
    iou_amount: str,  # e.g., "100" RLUSD
    max_xrp_to_send: str,  # e.g., "5000000" drops (5 XRP)
) -> str:
    # Create a cross-currency Payment transaction (XRP ➡ IOU)
    if not token_to_swap_for.currency or not token_to_swap_for.issuer:
        raise Exception("The token_to_swap_for's fields should not be empty")

    payment = Payment(
        account=sender_wallet.classic_address,
        destination=destination,
        amount=IssuedCurrencyAmount(
            currency=token_to_swap_for.currency, issuer=token_to_swap_for.issuer, value=iou_amount
        ),
        send_max=max_xrp_to_send,
        paths=[
            [
                token_to_swap_for,
            ]
        ],
        flags=131072,  # tfPartialPayment => presentation purpose => proof of risk
    )

    try:
        # sign and submit transaction
        signed_tx = await autofill_and_sign(payment, client, sender_wallet)
        tx = await submit_and_wait(signed_tx, client, sender_wallet)
    except XRPLReliableSubmissionException as e:
        raise Exception(f"Failed to submit payment: {e}")

    tx_data = TransactionData.model_validate(tx.result)
    return tx_data.hash
