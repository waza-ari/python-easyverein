"""
Member related models
"""
from __future__ import annotations

from typing import Literal

from pydantic import PositiveInt, Field

from .base import EasyVereinBase
from .mixins.required_attributes import required_mixin
from ..core.types import AnyHttpURL, Date, DateTime, EasyVereinReference


class Member(EasyVereinBase):
    """
    Pydantic model representing a Member

    Note that members cannot exist standalone. They must always be linked to a contact details instance,
    otherwise creation fails.

    Setting `isApplication` on creation automatically creates a membership application, which must be
    approved or denied in the portal.
    """

    profilePicture: AnyHttpURL | None = Field(default=None, alias="_profilePicture")
    joinDate: DateTime | None = None
    resignationDate: Date | None = None
    isChairman: bool | None = Field(default=None, alias="_isChairman")
    chairmanPermissionGroup: str | None = Field(
        default=None, alias="_chairmanPermissionGroup"
    )
    declarationOfApplication: AnyHttpURL | None = None
    declarationOfResignation: AnyHttpURL | None = None
    declarationOfConsent: AnyHttpURL | None = None
    membershipNumber: str | None = None
    contactDetails: ContactDetails | EasyVereinReference | None = None
    paymentStartDate: DateTime | None = Field(default=None, alias="_paymentStartDate")
    paymentAmount: float | None = None
    paymentIntervallMonths: PositiveInt | None = None
    useBalanceForMembershipFee: bool | None = None
    bulletinBoardNewPostNotification: bool | None = None
    integrationDosbGender: Literal["m", "w", "d"] | None = None
    isApplication: bool | None = Field(default=None, alias="_isApplication")
    applicationDate: Date | None = Field(default=None, alias="_applicationDate")
    applicationWasAcceptedAt: Date | None = Field(
        default=None, alias="_applicationWasAcceptedAt"
    )
    signatureText: str | None = None
    relatedMember: Member | EasyVereinReference | None = Field(
        default=None, alias="_relatedMember"
    )
    editableByRelatedMembers: bool | None = Field(
        default=None, alias="_editableByRelatedMembers"
    )
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
