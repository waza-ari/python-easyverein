from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from ..core.types import Date, EasyVereinReference, FilterIntList
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class MemberMemberGroupBase(EasyVereinBase):
    """
    This model represents a member group that is associated to a member. In addition
    to the association (which is always valid), it can be active or inactive in billing context,
    which is controlled by the `paymentActive` attribute and controls whether the billing settings
    of this group are considered for the member fee calculation.

    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `MemberMemberGroup` | `MemberMemberGroupCustomUpdate` | `MemberMemberGroupCreate` |
    """

    userObject: EasyVereinReference | Member | None = None
    memberGroup: EasyVereinReference | None = None
    paymentAmount: float | None = None
    paymentActive: bool = False
    start: Any | None = None  # Field not documented
    end: Any | None = None  # Field not documented


class MemberMemberGroup(MemberMemberGroupBase, EmptyStringsToNone):
    """
    Pydantic model representing a member custom field
    """

    pass


class MemberMemberGroupCreate(MemberMemberGroupBase, required_mixin(["memberGroup", "paymentActive"])):  # type: ignore
    """
    Pydantic model for creating a new member to member group association
    """


class MemberMemberGroupUpdate(MemberMemberGroupBase):
    """
    Pydantic model used to update a member group association
    """

    pass


class MemberMemberGroupFilter(BaseModel):
    id__in: FilterIntList | None = None
    paymentActive: bool | None = None
    start__gte: Date | None = None
    start__lte: Date | None = None
    start: Date | None = None
    end__gte: Date | None = None
    end__lte: Date | None = None
    end: Date | None = None
    deleted: bool | None = None
    memberGroup: int | None = None
    memberGroup__in: FilterIntList | None = None
    memberGroup__not: int | None = None
    showActiveGroups: bool | None = None
    ordering: int | None = None


from .member import Member  # noqa: E402
