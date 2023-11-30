"""
Invoice related models
"""
import datetime
from typing import Literal

from pydantic import BaseModel, PositiveInt

from ..core.types import AnyHttpUrl, Date, PositiveIntWithZero
from .invoice_item import InvoiceItem
from .mixins.required_attributes import required_mixin


class Invoice(BaseModel):
    """
    Pydantic model representing an Invoice
    """

    id: PositiveInt | None = None
    org: AnyHttpUrl | None = None
    _deleteAfterDate: datetime.date | None = None
    _deletedBy: str | None = None
    gross: bool | None = None
    canceledInvoice: str | None = None
    cancellationDescription: str | None = None
    templateName: str | None = None
    date: Date | None = None
    dateItHappend: datetime.date | None = None
    dateSent: datetime.date | None = None
    invNumber: str | None = None
    receiver: str | None = None
    description: str | None = None
    totalPrice: float | None = None
    tax: float | None = None
    taxRate: float | None = None
    taxName: str | None = None
    relatedAddress: AnyHttpUrl | None = None
    path: AnyHttpUrl | None = None
    kind: Literal[
        "balance", "donation", "membership", "revenue", "expense", "cancel", "credit"
    ] | None = None
    selectionAcc: AnyHttpUrl | None = None
    refNumber: str | None = None
    paymentDifference: float | None = None
    isDraft: bool | None = None
    isTemplate: bool | None = None
    paymentInformation: str | None = None
    isRequest: bool | None = None
    payedFromUser: AnyHttpUrl | None = None
    approvedFromAdmin: AnyHttpUrl | None = None
    actualCallStateName: str | None = None
    callStateDelayDays: PositiveIntWithZero | None = None
    accnumber: PositiveIntWithZero | None = None
    guid: str | None = None
    relatedBookings: list[AnyHttpUrl] | None = None
    invoiceItems: list[InvoiceItem] | list[AnyHttpUrl] | None = None


class InvoiceCreate(
    Invoice,
    required_mixin(["invNumber", "totalPrice", ["relatedAddress", "receiver"]]),
):
    """
    Pydantic model representing an Invoice
    """


class InvoiceUpdate(
    Invoice,
    required_mixin(["id", "invNumber", "totalPrice", ["relatedAddress", "receiver"]]),
):
    """
    Pydantic model representing an Invoice
    """
