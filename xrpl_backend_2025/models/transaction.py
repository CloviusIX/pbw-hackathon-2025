from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field


# === Amounts ===
class CurrencyAmount(BaseModel):
    currency: Annotated[str, Field(alias="currency")]
    issuer: Annotated[str, Field(alias="issuer")]
    value: Annotated[str, Field(alias="value")]


# === Memos ===
class Memo(BaseModel):
    memo_data: Annotated[Optional[str], Field(alias="MemoData", default=None)]


class MemoWrapper(BaseModel):
    memo: Annotated[Memo, Field(alias="Memo")]


# === Final/Previous/New Fields ===
class FinalFields(BaseModel):
    account: Annotated[Optional[str], Field(alias="Account", default=None)]
    balance: Annotated[Optional[Union[str, CurrencyAmount]], Field(alias="Balance", default=None)]
    flags: Annotated[Optional[int], Field(alias="Flags", default=None)]
    owner_count: Annotated[Optional[int], Field(alias="OwnerCount", default=None)]
    sequence: Annotated[Optional[int], Field(alias="Sequence", default=None)]
    amm_id: Annotated[Optional[str], Field(alias="AMMID", default=None)]
    high_limit: Annotated[Optional[CurrencyAmount], Field(alias="HighLimit", default=None)]
    low_limit: Annotated[Optional[CurrencyAmount], Field(alias="LowLimit", default=None)]
    high_node: Annotated[Optional[str], Field(alias="HighNode", default=None)]
    low_node: Annotated[Optional[str], Field(alias="LowNode", default=None)]
    owner: Annotated[Optional[str], Field(alias="Owner", default=None)]
    root_index: Annotated[Optional[str], Field(alias="RootIndex", default=None)]


class PreviousFields(BaseModel):
    balance: Annotated[Optional[Union[str, CurrencyAmount]], Field(alias="Balance", default=None)]
    owner_count: Annotated[Optional[int], Field(alias="OwnerCount", default=None)]
    sequence: Annotated[Optional[int], Field(alias="Sequence", default=None)]


class NewFields(BaseModel):
    account: Annotated[Optional[str], Field(alias="Account", default=None)]
    destination: Annotated[Optional[str], Field(alias="Destination", default=None)]
    invoice_id: Annotated[Optional[str], Field(alias="InvoiceID", default=None)]
    send_max: Annotated[Optional[CurrencyAmount], Field(alias="SendMax", default=None)]
    sequence: Annotated[Optional[int], Field(alias="Sequence", default=None)]


# === Ledger Nodes ===
class ModifiedNode(BaseModel):
    final_fields: Annotated[Optional[FinalFields], Field(alias="FinalFields", default=None)]
    ledger_entry_type: Annotated[str, Field(alias="LedgerEntryType")]
    ledger_index: Annotated[str, Field(alias="LedgerIndex")]
    previous_fields: Annotated[Optional[PreviousFields], Field(alias="PreviousFields", default=None)]
    previous_txn_id: Annotated[str, Field(alias="PreviousTxnID")]
    previous_txn_lgr_seq: Annotated[int, Field(alias="PreviousTxnLgrSeq")]


class CreatedNode(BaseModel):
    ledger_entry_type: Annotated[str, Field(alias="LedgerEntryType")]
    ledger_index: Annotated[str, Field(alias="LedgerIndex")]
    new_fields: Annotated[Optional[NewFields], Field(alias="NewFields", default=None)]


class AffectedNode(BaseModel):
    modified_node: Optional[ModifiedNode] = Field(default=None, alias="ModifiedNode")
    created_node: Optional[CreatedNode] = Field(default=None, alias="CreatedNode")


# === Meta ===
class Meta(BaseModel):
    affected_nodes: Annotated[List[AffectedNode], Field(alias="AffectedNodes")]
    transaction_index: Annotated[int, Field(alias="TransactionIndex")]
    transaction_result: Annotated[str, Field(alias="TransactionResult")]
    delivered_amount: Annotated[Optional[Union[str, CurrencyAmount]], Field(alias="delivered_amount", default=None)]


# === tx_json ===
class PathStep(BaseModel):
    currency: Optional[str]
    issuer: Optional[str]
    type: Optional[int]


class TxJson(BaseModel):
    account: Annotated[str, Field(alias="Account")]
    deliver_max: Annotated[Optional[Union[str, CurrencyAmount]], Field(alias="DeliverMax", default=None)]  # <-- FIXED
    destination: Annotated[str, Field(alias="Destination")]
    fee: Annotated[str, Field(alias="Fee")]
    flags: Annotated[int, Field(alias="Flags")]
    last_ledger_sequence: Annotated[int, Field(alias="LastLedgerSequence")]
    memos: Annotated[Optional[List[MemoWrapper]], Field(alias="Memos", default=None)]
    paths: Annotated[Optional[List[List[PathStep]]], Field(alias="Paths", default=None)]
    send_max: Annotated[Optional[Union[str, CurrencyAmount]], Field(alias="SendMax", default=None)]
    sequence: Annotated[int, Field(alias="Sequence")]
    signing_pub_key: Annotated[str, Field(alias="SigningPubKey")]
    transaction_type: Annotated[str, Field(alias="TransactionType")]
    txn_signature: Annotated[str, Field(alias="TxnSignature")]
    date: Annotated[int, Field(alias="date")]
    ledger_index: Annotated[int, Field(alias="ledger_index")]


# === Top-Level Transaction Container ===
class TransactionData(BaseModel):
    close_time_iso: Annotated[str, Field(alias="close_time_iso")]
    ctid: Annotated[str, Field(alias="ctid")]
    hash: Annotated[str, Field(alias="hash")]
    ledger_hash: Annotated[str, Field(alias="ledger_hash")]
    ledger_index: Annotated[int, Field(alias="ledger_index")]
    meta: Annotated[Meta, Field(alias="meta")]
    tx_json: Annotated[TxJson, Field(alias="tx_json")]
    validated: Annotated[bool, Field(alias="validated")]
