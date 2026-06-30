"""
ContactDetails related models
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..core.types import (
    FilterIntList,
    HexColor,
)
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class ContactDetailsGroupBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `ContactDetailsGroup` | `ContactDetailsGroupUpdate` | `ContactDetailsGroupCreate` |

    ContactDetails groups are used to categorize members into different groups.
    They can then be used to manage the members permissions, their membersip fee
    or to send out messages to specific groups of members.

    !!! info "ContactDetails Groups vs associations"
        This endpoint is used to manage the member groups themselves, not the assignment of members to groups.
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


class ContactDetailsGroupFilter(BaseModel):
    id__in: FilterIntList | None = None
    name: str | None = None
    color: HexColor | None = None
    short: str | None = None
    deleted: bool | None = None
    ordering: str | None = None
