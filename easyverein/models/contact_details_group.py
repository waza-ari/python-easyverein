"""
ContactDetailsGroup related models
"""

from __future__ import annotations

from pydantic import Field

from ..core.types import (
    FilterIntList,
    HexColor,
)
from .base import EasyVereinBase, EasyVereinFilter
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class ContactDetailsGroupBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `ContactDetailsGroup` | `ContactDetailsGroupUpdate` | `ContactDetailsGroupCreate` |

    Contact details groups are used to categorize contact details (addresses) into different groups.
    Contact details are assigned to groups via the `contactDetailsGroups` field of `ContactDetails`.

    !!! info "Contact details groups vs. assignments"
        This endpoint is used to manage the contact details groups themselves, not the assignment of
        contact details to groups.
    """

    name: str | None = Field(default=None, max_length=200)
    color: HexColor = None
    short: str | None = Field(default=None, max_length=4)


class ContactDetailsGroup(ContactDetailsGroupBase, EmptyStringsToNone):
    pass


class ContactDetailsGroupCreate(ContactDetailsGroupBase, required_mixin(["name", "color", "short"])):  # type: ignore
    pass


class ContactDetailsGroupUpdate(ContactDetailsGroupBase):
    pass


class ContactDetailsGroupFilter(EasyVereinFilter):
    id__in: FilterIntList | None = None
    name: str | None = None
    color: HexColor = None
    short: str | None = None
    deleted: bool | None = None
    ordering: str | None = None
