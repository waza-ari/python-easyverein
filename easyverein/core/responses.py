from typing import Any

from pydantic import BaseModel, ConfigDict
from requests import Response


class ResponseSchema(BaseModel):
    result: dict[str, Any] | list[dict[str, Any]] | None = None
    count: int | None = None
    response_code: int
    response: Response | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)