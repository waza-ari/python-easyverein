"""
Custom types used for model validation
"""

import datetime
import json
from typing import Annotated, Literal

from pydantic import Field, PlainSerializer, PlainValidator, UrlConstraints
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
    list[str] | str | None,
    PlainValidator(lambda x: json.loads(x) if isinstance(x, str) else x),
    PlainSerializer(lambda x: x if isinstance(x, str) else json.dumps(x), return_type=str),
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

Sphere = Literal[
    1, 2, 3, 4, 9,
    11, 12, 13, 14, 15, 16, 17, 18, 19,
    21, 22, 23, 24, 25, 26, 27, 28, 29,
    31, 32, 33, 34, 35, 36, 37, 38, 39,
    41, 42, 43, 44, 45, 46, 47, 48, 49,
]  # fmt: skip
"""
Sphere in the SKR 42 chart of accounts:

- 1: Ideeller Bereich
- 2: Vermögensverwaltung
- 3: Zweckbetrieb
- 4: Wirtschaftlicher Geschäftsbetrieb
- 9: Sammelposten
- 11-19, 21-29, 31-39, 41-49: Sub-spheres 1-9 of the respective sphere (e.g. 31 = Zweckbetrieb 1)
"""
