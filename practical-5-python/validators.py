"""Basic reusable validators for usernames, ages, and email addresses."""

import re

_USERNAME_PATTERN = re.compile(r"[A-Za-z0-9_]{3,20}\Z")
_EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+\Z"
)


def is_valid_username(username: object) -> bool:
    """Return whether username is 3-20 ASCII letters, digits, or underscores."""
    return isinstance(username, str) and _USERNAME_PATTERN.fullmatch(username) is not None


def is_valid_age(age: object) -> bool:
    """Return whether age is an integer from 0 through 120, excluding booleans."""
    return isinstance(age, int) and not isinstance(age, bool) and 0 <= age <= 120


def is_valid_email(email: object) -> bool:
    """Check a basic email format; this does not verify mailbox ownership."""
    if not isinstance(email, str) or email.startswith(".") or ".." in email:
        return False
    if "@" not in email:
        return False

    local_part = email.split("@", maxsplit=1)[0]
    if local_part.endswith("."):
        return False

    return _EMAIL_PATTERN.fullmatch(email) is not None
