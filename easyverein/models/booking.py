"""
Invoice Item model
"""

from __future__ import annotations

from pydantic import BaseModel

from ..core.types import DateTime, EasyVereinReference, FilterIntList
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class BookingBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `Booking` | `BookingUpdate` | `BookingCreate` |
    """

    amount: float | None = None
    # TODO: Add reference to BankAccount once implemented
    bankAccount: EasyVereinReference | None = None
    # TODO: Add reference to BillingAccount once implemented
    billingAccount: EasyVereinReference | None = None
    description: str | None = None
    date: DateTime | None = None
    receiver: str | None = None
    billingId: str | None = None
    blocked: bool | None = None
    paymentDifference: float | None = None
    counterpartIban: str | None = None
    counterpartBic: str | None = None
    twingleDonation: bool | None = None
    bookingProject: str | None = None
    sphere: int | None = None
    relatedInvoice: list[EasyVereinReference] | None = None


class Booking(BookingBase, EmptyStringsToNone):
    """
    Pydantic model representing an Booking
    """

    pass


class BookingCreate(
    BookingBase,
    required_mixin(["receiver", "date"]),  # type: ignore
):
    """
    Pydantic model representing a Booking
    """


class BookingUpdate(BookingBase):
    """
    Pydantic model used to patch an Booking
    """


class BookingFilter(BaseModel):
    """
    Pydantic model used to filter bookings
    """

    id__in: FilterIntList | None = None
    blocked: bool | None = None
    receiver: str | None = None
    receiver__ne: str | None = None
    billingId__in: FilterIntList | None = None
    billingId__isnull: bool | None = None
    paymentDifference: float | None = None
    paymentDifference__gte: float | None = None
    paymentDifference__lte: float | None = None
    paymentDifference__ne: float | None = None
    date: DateTime | None = None
    date__gt: DateTime | None = None
    date__lt: DateTime | None = None
    importDate: DateTime | None = None
    importDate__gt: DateTime | None = None
    importDate__lt: DateTime | None = None
    billingAccount__isnull: bool | None = None
    amount: float | None = None
    bankAccount: str | None = None
    bankAccount__name: str | None = None
    deleted: bool | None = None
    billingId__isempty: bool | None = None
    bookingprojectassignment: str | None = None
    bookingprojectassignment__not: str | None = None
    billingAccount: int | None = None
    billingAccount__not: int | None = None
    bookingProject: int | None = None
    bookingProject__not: int | None = None
    bookingProject__isnull: bool | None = None
    relatedInvoice__isnull: bool | None = None
    relatedInvoice: int | None = None
    search: str | None = None
