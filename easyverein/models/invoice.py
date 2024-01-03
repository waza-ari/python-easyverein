"""
Invoice related models
"""
from __future__ import annotations

from typing import Literal

from ..core.types import Date, EasyVereinReference, PositiveIntWithZero
from .base import EasyVereinBase
from .mixins.required_attributes import required_mixin


class Invoice(EasyVereinBase):
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
    # TODO: Add reference to ContactDetails once implemented
    relatedAddress: EasyVereinReference | None = None
    path: EasyVereinReference | None = None
    kind: Literal[
        "balance", "donation", "membership", "revenue", "expense", "cancel", "credit"
    ] | None = None
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


class InvoiceCreate(
    Invoice,
    required_mixin(["invNumber", "totalPrice", ["relatedAddress", "receiver"]]),
):
    """
    Pydantic model representing an Invoice
    """

    storedInS3: bool | None = None


class InvoiceUpdate(Invoice):
    """
    Pydantic model representing an Invoice
    """


from .invoice_item import InvoiceItem  # noqa: E402
from .member import Member  # noqa: E402
