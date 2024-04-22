"""
This module contains a generic plugin for Pydantic models that removes
empty strings and converts them to None.
"""

from typing import Any

from pydantic import model_validator


class EmptyStringsToNone:
    """
    Mixin class for Pydantic models
    """

    @model_validator(mode="before")
    def empty_string_to_none(cls, data: Any) -> Any:
        """
        Pydantic model validator, converting empty strings to None
        """
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str) and v == "":
                    data[k] = None
        return data
