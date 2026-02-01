from __future__ import annotations

from pydantic import BaseModel

from ..core.types import FilterIntList, FilterStrList, PositiveIntWithZero
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class CustomFieldSelectOptionBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `CustomFieldSelectOption` | `CustomFieldSelectOptionUpdate` | `CustomFieldSelectOptionCreate` |

    Custom field select options are used to define the possible values for a custom field.
    Those are only available for select (s) and multiselect (a) custom fields.
    """

    value: str
    orderSequence: PositiveIntWithZero | None = None
    availableForAssignment: bool | None = None


class CustomFieldSelectOption(CustomFieldSelectOptionBase, EmptyStringsToNone):
    """
    Pydantic model used to represent a custom field select option
    """

    pass


class CustomFieldSelectOptionCreate(CustomFieldSelectOptionBase, required_mixin(["value"])):  # type: ignore
    """
    Pydantic model for creating a new custom field select option
    """


class CustomFieldSelectOptionUpdate(CustomFieldSelectOptionBase):
    """
    Pydantic model used to update a custom field select option
    """

    pass


class CustomFieldSelectOptionFilter(BaseModel):
    """
    Pydantic model used to filter custom field select options
    """

    id__in: FilterIntList | None = None
    value: str | None = None
    value__in: FilterStrList | None = None
    maxSelections__isnull: bool | None = None
    maxSelections: PositiveIntWithZero | None = None
    orderSequence__isnull: bool | None = None
    orderSequence: PositiveIntWithZero | None = None
    actuallyRemoved: bool | None = None
