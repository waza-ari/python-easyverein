import json
from typing import Any


def empty_string_to_none(v: Any) -> Any:
    if isinstance(v, str) and v == "":
        return None
    return v


def parse_json_string(v: Any) -> Any:
    if isinstance(v, str):
        return json.loads(v)
    return v
