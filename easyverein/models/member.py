"""
Member related models
"""
from __future__ import annotations

from typing import Literal

from pydantic import Field, PositiveInt

from ..core.types import AnyHttpURL, Date, DateTime, EasyVereinReference
from .base import EasyVereinBase
from .mixins.required_attributes import required_mixin


class Member(EasyVereinBase):
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
    resignationDate: Date | None = None
    isChairman: bool | None = Field(default=None, alias="_isChairman")
    """
    Alias for `_isChairman` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    chairmanPermissionGroup: str | None = Field(
        default=None, alias="_chairmanPermissionGroup"
    )
    """
    Alias for `_chairmanPermissionGroup` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    declarationOfApplication: AnyHttpURL | None = None
    declarationOfResignation: AnyHttpURL | None = None
    declarationOfConsent: AnyHttpURL | None = None
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
    applicationWasAcceptedAt: Date | None = Field(
        default=None, alias="_applicationWasAcceptedAt"
    )
    """
    Alias for `_applicationWasAcceptedAt` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    signatureText: str | None = None
    relatedMember: Member | EasyVereinReference | None = Field(
        default=None, alias="_relatedMember"
    )
    """
    Alias for `_relatedMember` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    editableByRelatedMembers: bool | None = Field(
        default=None, alias="_editableByRelatedMembers"
    )
    """
    Alias for `_editableByRelatedMembers` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    sepaMandateFile: AnyHttpURL | None = None
    # TODO: exact type is not specified in API docs
    integrationDosbSport: list | None = None
    customFields: EasyVereinReference | list[MemberCustomField] | None = None


class MemberUpdate(Member):
    """
    Pydantic model used to update a member
    """

    profilePicture: AnyHttpURL | None = Field(
        default=None, serialization_alias="_profilePicture"
    )
    isChairman: bool | None = Field(default=None, serialization_alias="_isChairman")
    chairmanPermissionGroup: str | None = Field(
        default=None, serialization_alias="_chairmanPermissionGroup"
    )
    isApplication: bool | None = Field(
        default=None, serialization_alias="_isApplication"
    )

    pass


class MemberCreate(MemberUpdate, required_mixin(["contactDetails"])):
    """
    Pydantic model for creating a new member
    """


from .contact_details import ContactDetails  # noqa: E402
from .member_custom_field import MemberCustomField  # noqa: E402
