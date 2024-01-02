"""
Member related models
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, PositiveInt

from .mixins.required_attributes import required_mixin
from ..core.types import AnyHttpURL, Date, DateTime, EasyVereinReference


class Member(BaseModel):
    """
    Pydantic model representing a Member

    Note that members cannot exist standalone. They must always be linked to a contact details instance,
    otherwise creation fails.

    Setting `isApplication` on creation automatically creates a membership application, which must be
    approved or denied in the portal.
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None
    # TODO: Add reference to Organization once implemented
    _deleteAfterDate: Date | None = None
    _deletedBy: str | None = None
    _profilePicture: AnyHttpURL | None = None
    joinDate: DateTime | None = None
    resignationDate: Date | None = None
    _isChairman: bool | None = None
    _chairmanPermissionGroup: str | None
    declarationOfApplication: AnyHttpURL | None = None
    declarationOfResignation: AnyHttpURL | None = None
    declarationOfConsent: AnyHttpURL | None = None
    membershipNumber: str | None = None
    contactDetails: ContactDetails | EasyVereinReference | None = None
    _paymentStartDate: Date | None = None
    paymentAmount: float | None = None
    paymentIntervallMonths: PositiveInt | None = None
    useBalanceForMembershipFee: bool | None = None
    bulletinBoardNewPostNotification: bool | None = None
    integrationDosbGender: Literal["m", "w", "d"] | None = None
    _isApplication: bool | None = None
    _applicationDate: Date | None = None
    _applicationWasAcceptedAt: Date | None = None
    signatureText: str | None = None
    _relatedMember: Member | EasyVereinReference | None = None
    _editableByRelatedMembers: bool | None = None
    sepaMandateFile: AnyHttpURL | None = None
    # TODO: exact type is not specified in API docs
    integrationDosbSport: list | None = None
    customFields: EasyVereinReference | list[MemberCustomField] | None = None


class MemberCreate(Member, required_mixin(["contactDetails"])):
    """
    Pydantic model for creating a new member
    """


class MemberUpdate(Member):
    """
    Pydantic model used to update a member
    """

    pass


from .contact_details import ContactDetails  # noqa: E402
from .member_custom_field import MemberCustomField  # noqa: E402
