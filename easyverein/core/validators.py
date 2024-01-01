from typing import Any


def empty_string_to_none(v: Any) -> Any:
    if isinstance(v, str) and v == "":
        return None
    return v
