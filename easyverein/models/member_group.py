"""
Member related models
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, PositiveInt

from ..core.types import (
    EasyVereinReference,
    FilterIntList,
    HexColor,
    PositiveIntWithZero,
)
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class MemberGroupBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `MemberGroup` | `MemberGroupUpdate` | `MemberGroupCreate` |

    Member groups are used to categorize members into different groups.
    They can then be used to manage the members permissions, their membersip fee
    or to send out messages to specific groups of members.

    !!! info "Member Groups vs associations"
        This endpoint is used to manage the member groups themselves, not the assignment of members to groups.
    """

    name: str | None = Field(default=None, max_length=200)
    color: HexColor = None
    short: str | None = Field(default=None, max_length=4)
    userGroupAccount: EasyVereinReference | None = None
    paymentAmount: float | None = None
    assignmentDeleteAfterBooking: bool | None = None
    usePaymentFormula: bool | None = None
    paymentFormula: str | None = Field(default=None, max_length=512)
    paymentInterval: PositiveInt | None = None
    nameOnInvoice: str | None = Field(default=None, max_length=256)
    descriptionOnInvoice: str | None = None
    showInApplicationform: bool | None = None
    agePermission: PositiveIntWithZero | None = None
    nextGroup: EasyVereinReference | None = None
    taxRate: float | None = None
    billingAccount: EasyVereinReference | None = None
    costCentre: str | None = Field(default=None, max_length=8)
    isOnlyVisibleToAdmins: bool | None = None
    user_shares: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_bookings: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_protocols: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_members: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_members_groupaccess: Literal["n", "a", "d", "x"] | None = None
    """
    - n: standard
    - a: limited
    - d: unlimited
    - x: ignore group
    """
    user_membershipCte: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_edit: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_forum: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_board: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_boardLinks: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_importcalendar: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_invoiceRequest: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """
    user_inventory: Literal["n", "a", "d"] | None = None
    """
    - n: standard
    - a: allowed
    - d: forbidden
    """


class MemberGroup(MemberGroupBase, EmptyStringsToNone):
    pass


class MemberGroupCreate(MemberGroupBase, required_mixin(["name", "color", "short"])):  # type: ignore
    pass


class MemberGroupUpdate(MemberGroupBase):
    pass


class MemberGroupFilter(BaseModel):
    id__in: FilterIntList | None = None
    name: str | None = None
    paymentAmount: float | None = None
    paymentAmount__gt: float | None = None
    paymentAmount__lt: float | None = None
    kind: str | None = None
    deleted: bool | None = None
    ordering: str | None = None
