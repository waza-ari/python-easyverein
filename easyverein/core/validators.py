import json
from typing import Any


def parse_json_string(v: Any) -> Any:
    if isinstance(v, str):
        return json.loads(v)
    return v
