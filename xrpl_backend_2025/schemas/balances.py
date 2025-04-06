from pydantic import BaseModel


class BalanceRequest(BaseModel):
    seed: str
