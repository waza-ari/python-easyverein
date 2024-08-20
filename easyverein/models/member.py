"""
Member related models
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, PositiveInt

from ..core.types import (
    AnyHttpURL,
    Date,
    DateTime,
    EasyVereinReference,
    FilterIntList,
    FilterStrList,
)
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class MemberBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `Member` | `MemberUpdate` | `MemberCreate` |

    !!! info "Contact Details and Members"
        Note that contact details can be created standalone (independently of members), but members
        are required to have a contact details object linked.

    !!! info "Creating Membership Applications"
        Setting `isApplication` on creation automatically creates a membership application, which must be
        approved or denied in the portal.
    """

    profilePicture: AnyHttpURL | None = Field(default=None, alias="_profilePicture")
    """
    Alias for `_profilePicture` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    joinDate: DateTime | None = None
    resignationDate: DateTime | None = None
    isChairman: bool | None = Field(default=None, alias="_isChairman")
    """
    Alias for `_isChairman` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    chairmanPermissionGroup: str | None = Field(default=None, alias="_chairmanPermissionGroup")
    """
    Alias for `_chairmanPermissionGroup` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    declarationOfApplication: AnyHttpURL | str | None = None
    declarationOfResignation: AnyHttpURL | str | None = None
    declarationOfConsent: AnyHttpURL | str | None = None
    membershipNumber: str | None = None
    contactDetails: ContactDetails | EasyVereinReference | None = None
    paymentStartDate: DateTime | None = Field(default=None, alias="_paymentStartDate")
    """
    Alias for `_paymentStartDate` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    paymentAmount: float | None = None
    paymentIntervallMonths: PositiveInt | None = None
    useBalanceForMembershipFee: bool | None = None
    bulletinBoardNewPostNotification: bool | None = None
    integrationDosbGender: Literal["m", "w", "d"] | None = None
    isApplication: bool | None = Field(default=None, alias="_isApplication")
    """
    Alias for `_isApplication` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    applicationDate: Date | None = Field(default=None, alias="_applicationDate")
    """
    Alias for `_applicationDate` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    applicationWasAcceptedAt: Date | None = Field(default=None, alias="_applicationWasAcceptedAt")
    """
    Alias for `_applicationWasAcceptedAt` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    signatureText: str | None = None
    relatedMember: Member | EasyVereinReference | None = Field(default=None, alias="_relatedMember")
    """
    Alias for `_relatedMember` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    editableByRelatedMembers: bool | None = Field(default=None, alias="_editableByRelatedMembers")
    """
    Alias for `_editableByRelatedMembers` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    sepaMandateFile: AnyHttpURL | str | None = None
    # TODO: exact type is not specified in API docs
    integrationDosbSport: list | None = None
    customFields: EasyVereinReference | list[MemberCustomField] | None = None
    memberGroups: EasyVereinReference | list[MemberMemberGroup] | None = None


class Member(MemberBase, EmptyStringsToNone):
    """
    Pydantic model for members
    """

    pass


class MemberUpdate(MemberBase):
    """
    Pydantic model used to update a member
    """

    profilePicture: AnyHttpURL | None = Field(default=None, serialization_alias="_profilePicture")
    isChairman: bool | None = Field(default=None, serialization_alias="_isChairman")
    chairmanPermissionGroup: str | None = Field(default=None, serialization_alias="_chairmanPermissionGroup")
    isApplication: bool | None = Field(default=None, serialization_alias="_isApplication")
    paymentStartDate: DateTime | None = Field(default=None, serialization_alias="_paymentStartDate")


class MemberCreate(MemberUpdate, required_mixin(["contactDetails"])):  # type: ignore
    """
    Pydantic model for creating a new member
    """

    emailOrUserName: str


class MemberFilter(BaseModel):
    """
    Pydantic model used to filter members
    """

    id__in: FilterIntList | None = None
    paymentAmount__gt: float | None = None
    paymentAmount__lt: float | None = None
    paymentAmount: float | None = None
    paymentAmount__ne: float | None = None
    email: str | None = None
    email__ne: str | None = None
    contactDetails: str | None = None
    contactDetails__preferredCommunicationWay: int | None = None
    contactDetails__preferredCommunicationWay__ne: int | None = None
    contactDetails__country: str | None = None
    membershipNumber: str | None = None
    membershipNumber__in: FilterStrList | None = None
    deletedBy: int = Field(default=None, serialization_alias="_deletedBy")
    deletedBy__ne: int = Field(default=None, serialization_alias="_deletedBy__ne")
    deletedBy__isnull: bool = Field(default=None, serialization_alias="_deletedBy__isnull")
    joinDate: DateTime | None = None
    joinDate__gte: DateTime | None = None
    joinDate__lte: DateTime | None = None
    joinDate__isnull: DateTime | None = None
    resignationDate: DateTime | None = None
    resignationDate__gte: DateTime | None = None
    resignationDate__lte: DateTime | None = None
    resignationDate__isnull: DateTime | None = None
    isApplication: bool = Field(default=None, serialization_alias="_isApplication")
    applicationDate: Date = Field(default=None, serialization_alias="_applicationDate")
    applicationDate__gte: Date = Field(default=None, serialization_alias="_applicationDate__gte")
    applicationDate__lte: Date = Field(default=None, serialization_alias="_applicationDate__lte")
    applicationDate__isnull: Date = Field(default=None, serialization_alias="_applicationDate__isnull")
    applicationWasAcceptedAt: Date = Field(default=None, serialization_alias="_applicationWasAcceptedAt")
    applicationWasAcceptedAt__gte: Date = Field(default=None, serialization_alias="_applicationWasAcceptedAt__gte")
    applicationWasAcceptedAt__lte: Date = Field(default=None, serialization_alias="_applicationWasAcceptedAt__lte")
    applicationWasAcceptedAt__isnull: bool = Field(
        default=None, serialization_alias="_applicationWasAcceptedAt__isnull"
    )
    isChairman: bool = Field(default=None, serialization_alias="_isChairman")
    memberGroups: FilterIntList | None = None
    """
    Filter for members that are member of the given group(s)
    """
    memberGroups__not: FilterIntList | None = None
    """
    Filter for members that are not member in any of the given group(s)
    """
    memberGroupsCurrentlyActive: int | None = None
    """
    Filter for members that are member of the given group and the group is actively used for billing purposes
    """
    deleted: bool | None = None
    custom_field_name: str | None = None
    custom_field_value: str | None = None
    custom_field_value__in: FilterStrList | None = None
    custom_field_value__not_in: FilterStrList | None = None
    ordering: str | None = None
    showOnlyUpcomingBirthdays: bool | None = None
    showOnlyUpcomingAnniversaries: bool | None = None
    hasCopyInOrg: str | None = None
    hasCopyInOrg__not: str | None = None
    isCopy: bool | None = None
    hasCopy: bool | None = None
    search: str | None = None


from .contact_details import ContactDetails  # noqa: E402
from .member_custom_field import MemberCustomField  # noqa: E402
from .member_member_group import MemberMemberGroup  # noqa: E402
