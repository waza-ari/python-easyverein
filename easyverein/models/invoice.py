"""
Invoice related models
"""
from typing import Literal

from pydantic import BaseModel, PositiveInt

from ..core.types import Date, EasyVereinReference, PositiveIntWithZero
from .invoice_item import InvoiceItem
from .mixins.required_attributes import required_mixin


class Invoice(BaseModel):
    """
    Pydantic model representing an Invoice
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None
    _deleteAfterDate: Date | None = None
    _deletedBy: str | None = None
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
    relatedAddress: EasyVereinReference | None = None
    path: EasyVereinReference | None = None
    kind: Literal[
        "balance", "donation", "membership", "revenue", "expense", "cancel", "credit"
    ] | None = None
    selectionAcc: EasyVereinReference | None = None
    refNumber: str | None = None
    paymentDifference: float | None = None
    isDraft: bool | None = None
    isTemplate: bool | None = None
    paymentInformation: str | None = None
    isRequest: bool | None = None
    payedFromUser: EasyVereinReference | None = None
    approvedFromAdmin: EasyVereinReference | None = None
    actualCallStateName: str | None = None
    callStateDelayDays: PositiveIntWithZero | None = None
    accnumber: PositiveIntWithZero | None = None
    guid: str | None = None
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
