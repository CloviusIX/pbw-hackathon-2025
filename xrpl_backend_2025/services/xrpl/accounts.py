from typing import Optional

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models import AccountInfo, AccountObjects, AccountObjectType

from xrpl_backend_2025.models.account_info import PydanticAccountInfo
from xrpl_backend_2025.models.account_objects import AccountObjectsData


async def get_account_info(client: AsyncJsonRpcClient, wallet_address: str) -> PydanticAccountInfo:
    account_info = AccountInfo(account=wallet_address, ledger_index="validated")
    resp = await client.request(account_info)
    account = PydanticAccountInfo.model_validate(resp.result)
    return account


async def get_account_objects(client: AsyncJsonRpcClient, destination: str) -> AccountObjectsData:
    account_object = AccountObjects(account=destination, type=AccountObjectType.CHECK, ledger_index="validated")
    response = await client.request(account_object)

    account = AccountObjectsData.model_validate(response.result)
    return account


async def get_check_id(account: AccountObjectsData) -> Optional[str]:
    check_id = account.account_objects and account.account_objects[0].index or None
    return check_id
