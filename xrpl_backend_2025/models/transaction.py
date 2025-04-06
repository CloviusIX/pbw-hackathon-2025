from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


# === Currency ===
class SendMax(BaseModel):
    currency: Annotated[str, Field(alias="currency")]
    issuer: Annotated[str, Field(alias="issuer")]
    value: Annotated[str, Field(alias="value")]


# === Memos ===
class Memo(BaseModel):
    memo_data: Annotated[Optional[str], Field(alias="MemoData", default=None)]


class MemoWrapper(BaseModel):
    memo: Annotated[Memo, Field(alias="Memo")]


# === Fields used across multiple node types ===
class FinalFields(BaseModel):
    account: Annotated[Optional[str], Field(alias="Account", default=None)]
    balance: Annotated[Optional[str], Field(alias="Balance", default=None)]
    flags: Annotated[Optional[int], Field(alias="Flags", default=None)]
    owner_count: Annotated[Optional[int], Field(alias="OwnerCount", default=None)]
    sequence: Annotated[Optional[int], Field(alias="Sequence", default=None)]
    owner: Annotated[Optional[str], Field(alias="Owner", default=None)]
    root_index: Annotated[Optional[str], Field(alias="RootIndex", default=None)]


class PreviousFields(BaseModel):
    balance: Annotated[Optional[str], Field(alias="Balance", default=None)]
    owner_count: Annotated[Optional[int], Field(alias="OwnerCount", default=None)]
    sequence: Annotated[Optional[int], Field(alias="Sequence", default=None)]


class NewFields(BaseModel):
    account: Annotated[Optional[str], Field(alias="Account", default=None)]
    destination: Annotated[Optional[str], Field(alias="Destination", default=None)]
    invoice_id: Annotated[Optional[str], Field(alias="InvoiceID", default=None)]
    send_max: Annotated[Optional[SendMax], Field(alias="SendMax", default=None)]
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
    # deleted_node: Optional[DeletedNode] = Field(default=None, alias="DeletedNode")  # You can add this if needed


# === Metadata (meta) ===
class Meta(BaseModel):
    affected_nodes: Annotated[List[AffectedNode], Field(alias="AffectedNodes")]
    transaction_index: Annotated[int, Field(alias="TransactionIndex")]
    transaction_result: Annotated[str, Field(alias="TransactionResult")]
    delivered_amount: Optional[str] = Field(default=None, alias="delivered_amount")


# === Transaction JSON (tx_json) ===
class TxJson(BaseModel):
    account: Annotated[str, Field(alias="Account")]
    destination: Annotated[str, Field(alias="Destination")]
    fee: Annotated[str, Field(alias="Fee")]
    flags: Annotated[int, Field(alias="Flags")]
    invoice_id: Annotated[Optional[str], Field(alias="InvoiceID", default=None)]
    last_ledger_sequence: Annotated[int, Field(alias="LastLedgerSequence")]
    memos: Annotated[Optional[List[MemoWrapper]], Field(alias="Memos", default=None)]
    send_max: Annotated[Optional[SendMax], Field(alias="SendMax", default=None)]
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
