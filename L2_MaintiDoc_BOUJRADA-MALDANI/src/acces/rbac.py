"""
RBAC access control – pre-filter helper for Qdrant queries.
"""
from __future__ import annotations
import hashlib, hmac, re
from src.config import RBAC, HMAC_SECRET


def get_allowed_families(user_group: str) -> list[str]:
    role = RBAC.get(user_group)
    if not role:
        return []
    return role["allowed_families"]


def check_access(user_group: str, famille: str) -> bool:
    return famille in get_allowed_families(user_group)


def forge_token(doc_id: str) -> str:
    return hmac.new(HMAC_SECRET.encode(), doc_id.encode(), hashlib.sha256).hexdigest()


def verify_token(doc_id: str, token: str) -> bool:
    expected = hmac.new(HMAC_SECRET.encode(), doc_id.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, token)


_INJECTION_PATTERNS = re.compile(
    r"(ignore\s+previous|system\s*prompt|<\s*script|drop\s+table)", re.I
)


def sanitize(text: str) -> tuple[str, bool]:
    """Return (cleaned_text, was_flagged)."""
    flagged = bool(_INJECTION_PATTERNS.search(text))
    clean = _INJECTION_PATTERNS.sub("[REDACTED]", text)
    return clean, flagged
