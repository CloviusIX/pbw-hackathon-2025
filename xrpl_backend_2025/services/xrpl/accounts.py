from decimal import Decimal

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models import AccountInfo, AccountObjects, AccountObjectType
from xrpl.utils import drops_to_xrp

from xrpl_backend_2025.models.account_info import AccountInfoData
from xrpl_backend_2025.models.account_objects import AccountObjectsData


async def get_account_info(client: AsyncJsonRpcClient, wallet_address: str) -> AccountInfoData:
    account_info = AccountInfo(account=wallet_address, ledger_index="validated")
    resp = await client.request(account_info)
    account = AccountInfoData.model_validate(resp.result)
    return account


async def get_account_objects(client: AsyncJsonRpcClient, destination: str) -> AccountObjectsData:
    account_object = AccountObjects(account=destination, type=AccountObjectType.CHECK, ledger_index="validated")
    response = await client.request(account_object)

    account = AccountObjectsData.model_validate(response.result)
    return account


async def get_check_id(account: AccountObjectsData) -> str:
    check_id = account.account_objects and account.account_objects[0].index or ""
    return check_id


async def get_xrp_balance(account_info: AccountInfoData) -> Decimal:
    return drops_to_xrp(account_info.account_data.balance)
