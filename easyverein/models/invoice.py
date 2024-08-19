"""
Invoice related models
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from ..core.types import (
    Date,
    EasyVereinReference,
    FilterIntList,
    FilterStrList,
    PositiveIntWithZero,
)
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class InvoiceBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `Invoice` | `InvoiceUpdate` | `InvoiceCreate` |
    """

    gross: bool | None = None
    canceledInvoice: str | None = None
    cancellationDescription: str | None = None
    templateName: str | None = None
    date: Date | None = None
    dateItHappend: Date | None = None
    dateSent: Date | None = None
    invNumber: str | None = None
    receiver: str | None = None
    description: str | None = None
    totalPrice: float | None = None
    tax: float | None = None
    taxRate: float | None = None
    taxName: str | None = None
    relatedAddress: ContactDetails | EasyVereinReference | None = None
    path: EasyVereinReference | None = None
    kind: (
        Literal[
            "balance",
            "donation",
            "membership",
            "revenue",
            "expense",
            "cancel",
            "credit",
        ]
        | None
    ) = None
    # TODO: Add reference to BillingAccount once implemented
    selectionAcc: EasyVereinReference | None = None
    refNumber: str | None = None
    paymentDifference: float | None = None
    isDraft: bool | None = None
    isTemplate: bool | None = None
    paymentInformation: str | None = None
    isRequest: bool | None = None
    payedFromUser: Member | EasyVereinReference | None = None
    approvedFromAdmin: Member | EasyVereinReference | None = None
    actualCallStateName: str | None = None
    callStateDelayDays: PositiveIntWithZero | None = None
    accnumber: PositiveIntWithZero | None = None
    guid: str | None = None
    # TODO: Add reference to Booking once implemented
    relatedBookings: list[EasyVereinReference] | None = None
    invoiceItems: list[InvoiceItem] | list[EasyVereinReference] | None = None


class Invoice(InvoiceBase, EmptyStringsToNone):
    """
    Pydantic model representing an Invoice
    """

    pass


class InvoiceCreate(
    InvoiceBase,
    required_mixin(["invNumber", "totalPrice", ["relatedAddress", "receiver"]]),  # type: ignore
):
    """
    Pydantic model representing an Invoice
    """

    storedInS3: bool | None = None


class InvoiceUpdate(InvoiceBase):
    """
    Pydantic model representing an Invoice
    """


class InvoiceFilter(BaseModel):
    """
    Pydantic model used to filter invoices
    """

    id__in: FilterIntList | None = None
    relatedAddress: int | None = None
    relatedAddress__isnull: bool | None = None
    relatedBookings: FilterIntList | None = None
    relatedBookings__isnull: bool | None = None
    relatedBookings__ne: FilterIntList | None = None
    payedFromUser: int | None = None
    payedFromUser__isnull: bool | None = None
    approvedFromAdmin: int | None = None
    approvedFromAdmin__isnull: bool | None = None
    canceledInvoice__isnull: bool | None = None
    date: Date | None = None
    date__gt: Date | None = None
    date__lt: Date | None = None
    dateItHappened: Date | None = None
    dateItHappened__gt: Date | None = None
    dateItHappened__lt: Date | None = None
    invNumber__in: FilterStrList | None = None
    receiver: str | None = None
    totalPrice: float | None = None
    totalPrice__gte: float | None = None
    totalPrice__lte: float | None = None
    kind: str | None = None
    kind__in: FilterStrList | None = None
    refNumber: str | None = None
    paymentDifference: float | None = None
    paymentDifference__gte: float | None = None
    paymentDifference__lte: float | None = None
    paymentDifference__ne: float | None = None
    isRequest: bool | None = None
    accnumber: int | None = None
    accnumber__ne: int | None = None
    isDraft: bool | None = None
    isTemplate: bool | None = None
    actualCallStateName: str | None = None
    actualCallStateName__ne: str | None = None
    deleted: bool | None = None
    customfilter: int | None = None
    usesessionfilter: bool | None = None
    ordering: str | None = None
    search: str | None = None


from .contact_details import ContactDetails  # noqa: E402
from .invoice_item import InvoiceItem  # noqa: E402
from .member import Member  # noqa: E402
