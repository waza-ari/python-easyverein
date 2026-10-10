"""
Helpers dealing with the differences between the supported EasyVerein API versions.

The Python models of this library use the (camelCase) field names of API v2.0. API v3.0 renamed every field,
filter and query parameter to snake_case and removed leading underscores. Instead of maintaining a second set of
models, the library translates names on the wire. The helpers in this module implement the naming rules that are
shared by models, filters, queries and orderings.
"""

import re
from typing import Final

API_V2: Final = "v2.0"
API_V3: Final = "v3.0"

SUPPORTED_API_VERSIONS: Final = [API_V2, API_V3]
"""API versions supported by this library. The first entry is the default."""

DEFAULT_API_VERSION: Final = API_V2

REMOVED_API_VERSIONS: Final = {
    "v1.7": "API v1.7 is deprecated by EasyVerein and no longer supported. "
    "Use API v2.0 or v3.0, or pin python-easyverein to version 1.x.",
}

API_VERSION_CONTEXT_KEY: Final = "api_version"
"""Key used in Pydantic validation / serialization contexts to pass the API version to the models."""

QUERY_RENAMES: Final = {
    "geoPositionCoords": "geo_position_coordinates",
}
"""Field names that were not only converted to snake_case in v3.0, but renamed entirely."""

COUNT_PARAM: Final = {API_V2: "showCount", API_V3: "show_count"}
"""
URL parameter instructing the API to include the total count in list responses.
Not covered by the v3.0 changelog: v3.0 silently ignores `showCount`.
"""

TOKEN_REFRESH_HEADER: Final = {API_V2: "tokenRefreshNeeded", API_V3: "token_refresh_needed"}
"""Response header indicating that the API token should be refreshed."""

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def to_snake_case(name: str) -> str:
    """
    Converts an API v2.0 field name to its API v3.0 counterpart.

    Leading underscores are removed, camelCase is converted to snake_case and acronyms are treated as one word,
    e.g. `_isCompany` -> `is_company`, `user_allowICSExport` -> `user_allow_ics_export`. Lookups separated by
    double underscores (`contactDetails__firstName__ne`) are preserved. Names that are already in snake_case
    are returned unchanged.
    """
    name = name.lstrip("_")
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def translate_query(query: str, api_version: str) -> str:
    """
    Translates a query (e.g. `{id,contactDetails{firstName,_isCompany}}`) or an `ordering` value
    (e.g. `-invNumber,date`) into the naming of the given API version.

    Queries for v3.0 can therefore be written using either the v2.0 (camelCase) or the v3.0 (snake_case) names.
    """
    if not query or api_version != API_V3:
        return query
    return _IDENTIFIER.sub(lambda m: QUERY_RENAMES.get(m.group(0), to_snake_case(m.group(0))), query)
