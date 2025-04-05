from typing import Optional

from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: int
    destination: str
    seed: str


class PaymentRequest(PaymentBase):
    pass


class PaymentResponse(BaseModel):
    hash: str
    balance: int


# For IOU checks with memo/invoice_id
class CheckRequest(PaymentBase):
    memo: Optional[str]
    invoice_id: Optional[str]


class CheckResponse(BaseModel):
    check_hash: Optional[str]
    check_id: Optional[str]
