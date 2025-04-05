from typing import Annotated

from pydantic import BaseModel, Field


class AccountData(BaseModel):
    account: Annotated[str, Field(alias="Account")]
    balance: Annotated[str, Field(alias="Balance")]
    flags: Annotated[int, Field(alias="Flags")]
    ledger_entry_type: Annotated[str, Field(alias="LedgerEntryType")]
    owner_count: Annotated[int, Field(alias="OwnerCount")]
    previous_txn_id: Annotated[str, Field(alias="PreviousTxnID")]
    previous_txn_lgr_seq: Annotated[int, Field(alias="PreviousTxnLgrSeq")]
    sequence: Annotated[int, Field(alias="Sequence")]
    index: Annotated[str, Field(alias="index")]


class AccountFlags(BaseModel):
    allow_trust_line_clawback: Annotated[bool, Field(alias="allowTrustLineClawback")]
    default_ripple: Annotated[bool, Field(alias="defaultRipple")]
    deposit_auth: Annotated[bool, Field(alias="depositAuth")]
    disable_master_key: Annotated[bool, Field(alias="disableMasterKey")]
    disallow_incoming_check: Annotated[bool, Field(alias="disallowIncomingCheck")]
    disallow_incoming_nftoken_offer: Annotated[bool, Field(alias="disallowIncomingNFTokenOffer")]
    disallow_incoming_pay_chan: Annotated[bool, Field(alias="disallowIncomingPayChan")]
    disallow_incoming_trustline: Annotated[bool, Field(alias="disallowIncomingTrustline")]
    disallow_incoming_xrp: Annotated[bool, Field(alias="disallowIncomingXRP")]
    global_freeze: Annotated[bool, Field(alias="globalFreeze")]
    no_freeze: Annotated[bool, Field(alias="noFreeze")]
    password_spent: Annotated[bool, Field(alias="passwordSpent")]
    require_authorization: Annotated[bool, Field(alias="requireAuthorization")]
    require_destination_tag: Annotated[bool, Field(alias="requireDestinationTag")]


class PydanticAccountInfo(BaseModel):
    account_data: AccountData
    account_flags: AccountFlags
    ledger_hash: str
    ledger_index: int
    validated: bool
