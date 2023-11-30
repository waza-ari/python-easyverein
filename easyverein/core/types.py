"""
Custom types used for model validation
"""
import datetime
from typing import Annotated

from pydantic import Field, PlainSerializer, UrlConstraints
from pydantic_core import Url

AnyHttpUrl = Annotated[Url, UrlConstraints(allowed_schemes=["http", "https"])]
PositiveIntWithZero = Annotated[int, Field(ge=0)]
Date = Annotated[
    datetime.date, PlainSerializer(lambda x: x.strftime("%Y-%m-%d"), return_type=str)
]
