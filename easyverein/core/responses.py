from typing import Generic, TypeVar

from pydantic import BaseModel
from requests import Response

T = TypeVar("T", bound=BaseModel)


class ResponseSchema(BaseModel, Generic[T]):
    result: list[T] | T
    count: int
    response: Response | None = None
