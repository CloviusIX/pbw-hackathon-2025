from typing import Annotated, List

from pydantic import BaseModel, Field


class SendMax(BaseModel):
    currency: Annotated[str, Field(alias="currency")]
    issuer: Annotated[str, Field(alias="issuer")]
    value: Annotated[str, Field(alias="value")]


class AccountObject(BaseModel):
    account: Annotated[str, Field(alias="Account")]
    destination: Annotated[str, Field(alias="Destination")]
    destination_node: Annotated[str, Field(alias="DestinationNode")]
    flags: Annotated[int, Field(alias="Flags")]
    ledger_entry_type: Annotated[str, Field(alias="LedgerEntryType")]
    owner_node: Annotated[str, Field(alias="OwnerNode")]
    previous_txn_id: Annotated[str, Field(alias="PreviousTxnID")]
    previous_txn_lgr_seq: Annotated[int, Field(alias="PreviousTxnLgrSeq")]
    send_max: Annotated[SendMax, Field(alias="SendMax")]
    sequence: Annotated[int, Field(alias="Sequence")]
    index: Annotated[str, Field(alias="index")]


class AccountObjectsData(BaseModel):
    account: Annotated[str, Field(alias="account")]
    account_objects: Annotated[List[AccountObject], Field(alias="account_objects")]
    ledger_current_index: Annotated[int, Field(alias="ledger_current_index")]
    validated: Annotated[bool, Field(alias="validated")]
