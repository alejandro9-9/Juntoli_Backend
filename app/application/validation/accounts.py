from app.application.common.validation import fail, require_text, require_timezone
from app.domain.entities import Role, User


def validate_user(user: User) -> None:
    require_text(user.name, "name")
    require_text(user.email, "email")
    require_text(user.password_hash, "password_hash")
    if "@" not in user.email or user.email.startswith("@") or user.email.endswith("@"):
        fail("email must be valid")
    require_timezone(user.created_at, "created_at")


def validate_role(role: Role) -> None:
    require_text(role.name, "name")
