from datetime import datetime
from decimal import Decimal

from app.application.common.exceptions import ApplicationValidationError


def fail(message: str) -> None:
    raise ApplicationValidationError(message)


def require_text(value: str, field_name: str) -> None:
    if not value.strip():
        fail(f"{field_name} cannot be empty")


def require_non_negative(value: Decimal, field_name: str) -> None:
    if value < 0:
        fail(f"{field_name} cannot be negative")


def require_timezone(value: datetime | None, field_name: str) -> None:
    if value is not None and (value.tzinfo is None or value.utcoffset() is None):
        fail(f"{field_name} must be timezone-aware")
