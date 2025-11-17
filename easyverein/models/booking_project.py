"""
BookingProject model
"""

from __future__ import annotations

from pydantic import BaseModel

from ..core.types import FilterIntList
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class BookingProjectBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `BookingProject` | `BookingProjectUpdate` | `BookingProjectCreate` |
    """

    name: str | None = None
    color: str | None = None
    short: str | None = None
    budget: str | None = None
    completed: bool | None = None
    projectCostCentre: str | None = None


class BookingProject(BookingProjectBase, EmptyStringsToNone):
    """
    Pydantic model representing a BookingProject
    """

    pass


class BookingProjectCreate(
    BookingProjectBase,
    required_mixin(["name"]),
):
    """
    Pydantic model for creating a BookingProject
    """


class BookingProjectUpdate(BookingProjectBase):
    """
    Pydantic model used to patch a BookingProject
    """


class BookingProjectFilter(BaseModel):
    """
    Pydantic model used to filter booking projects
    """

    id__in: FilterIntList | None = None
    budget__lt: float | None = None
    budget__gt: float | None = None
    name: str | None = None
    short: str | None = None
    completed: bool | None = None
