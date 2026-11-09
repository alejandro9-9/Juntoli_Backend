from collections.abc import Iterable
from uuid import UUID

from app.application.validation.profiles import validate_category_ids
from app.domain.entities import Brand


def update_brand_categories(
    brand: Brand,
    category_ids: Iterable[UUID],
) -> None:
    updated_category_ids = frozenset(category_ids)
    validate_category_ids(updated_category_ids, "brand")
    brand.category_ids = updated_category_ids
