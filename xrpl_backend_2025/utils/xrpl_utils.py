import hashlib

from xrpl.models import Memo


def to_hex_memo(note: str) -> Memo:
    return Memo(memo_data=note.encode("utf-8").hex().upper())


def to_invoice_id(input_string: str) -> str:
    hash_bytes = hashlib.sha256(input_string.encode("utf-8")).digest()
    return hash_bytes.hex().upper()  # XRPL style: hex string in uppercase
