"""
Member related models
"""
from typing import Literal

from pydantic import BaseModel, PositiveInt

from ..core.types import AnyHttpURL, Date, DateTime, EasyVereinReference


class Member(BaseModel):
    """
    Pydantic model representing an Invoice
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None
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
    # TODO: Add model once implemented
    contactDetails: EasyVereinReference | None = None
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
    _relatedMember: EasyVereinReference | None = None
    _editableByRelatedMembers: bool | None = None
    sepaMandateFile: AnyHttpURL | None = None
    # TODO: exact type is not specified in API docs
    integrationDosbSport: list | None = None
