from collections.abc import Collection
from uuid import UUID

from app.application.common.validation import fail, require_text, require_timezone
from app.domain.entities import Brand, Category, Creator


def validate_category_ids(category_ids: Collection[UUID], owner_name: str) -> None:
    if len(category_ids) > 3:
        fail(f"a {owner_name} can have at most three categories")


def validate_category(category: Category) -> None:
    require_text(category.name, "name")


def validate_brand(brand: Brand) -> None:
    require_text(brand.name, "name")
    validate_category_ids(brand.category_ids, "brand")
    require_timezone(brand.created_at, "created_at")


def validate_creator(creator: Creator) -> None:
    require_text(creator.public_name, "public_name")
    validate_category_ids(creator.category_ids, "creator")
    require_timezone(creator.created_at, "created_at")
