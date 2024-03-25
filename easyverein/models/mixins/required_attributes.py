"""
This module contains a class factory returning a Mixin class
"""

from typing import Self

from pydantic import BaseModel, model_validator


def required_mixin(required_attributes: list[str | list[str]]):
    """
    This method is a class factory returning a Mixin class
    for Pydantic models. It makes sure that certain attributes
    are set.

    Args:
        required_attributes (list[str | list[str]]): list of required attribute names.
            Each element of the list can either be a plain string (in which case
            the attribute is required) or a list of strings (in which case one of
            the attributes must be set)

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    class SomeRequired(BaseModel):
        """
        Mixin class for Pydantic models
        """

        @model_validator(mode="after")
        def required_fields(self) -> Self:
            """
            Pydantic model validator, requiring certain fields to be not None
            """
            for v in required_attributes:
                if isinstance(v, str):
                    if getattr(self, v) is None:
                        raise ValueError(f"{v} attribute is required but is None")
                else:
                    if not any(getattr(self, attr) is not None for attr in v):
                        raise ValueError(f"One of {v} is required.")

            return self

    return SomeRequired
