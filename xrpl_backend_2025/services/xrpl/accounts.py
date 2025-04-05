from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models import AccountInfo

from xrpl_backend_2025.models.account_info import PydanticAccountInfo


async def get_account_info(client: AsyncJsonRpcClient, wallet_address: str) -> PydanticAccountInfo:
    account_info = AccountInfo(account=wallet_address, ledger_index="validated")
    resp = await client.request(account_info)
    account = PydanticAccountInfo.model_validate(resp.result)
    return account
