"""
Custom types used for model validation
"""

import datetime
import json
from typing import Annotated

from pydantic import Field, PlainSerializer, UrlConstraints
from pydantic_core import Url

AnyHttpURL = Annotated[
    Url,
    UrlConstraints(allowed_schemes=["http", "https"]),
    PlainSerializer(lambda x: str(x), return_type=str),
]
EasyVereinReference = int | AnyHttpURL | None
PositiveIntWithZero = Annotated[int, Field(ge=0)]
Date = Annotated[datetime.date, PlainSerializer(lambda x: x.strftime("%Y-%m-%d"), return_type=str)]
DateTime = Annotated[
    datetime.datetime,
    PlainSerializer(lambda x: x.strftime("%Y-%m-%dT%H:%M:%S"), return_type=str),
]
OptionsField = Annotated[
    list[str] | None,
    PlainSerializer(lambda x: json.dumps(x), return_type=str),
]
HexColor = Annotated[
    str | None,
    Field(min_length=7, max_length=7),
]

FilterIntList = Annotated[
    list[int],
    PlainSerializer(lambda x: ",".join([str(i) for i in x]), return_type=str),
]

FilterStrList = Annotated[
    list[str],
    PlainSerializer(lambda x: ",".join(x), return_type=str),
]
