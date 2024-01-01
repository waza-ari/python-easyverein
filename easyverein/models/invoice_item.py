"""
Invoice Item model
"""
from typing import Annotated

from pydantic import BaseModel, PositiveInt, StringConstraints

from ..core.types import EasyVereinReference
from .mixins.required_attributes import required_mixin


class InvoiceItem(BaseModel):
    """
    Pydantic model representing an Invoice
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None
    relatedInvoice: EasyVereinReference | None = None
    quantity: PositiveInt | None = None
    unitPrice: float | None = None
    totalPrice: float | None = None
    title: str | None = None
    description: str | None = None
    taxRate: float | None = None
    gross: bool | None = None
    taxName: str | None = None
    billingAccount: EasyVereinReference | None = None
    costCentre: Annotated[str, StringConstraints(max_length=8)] | None = None


class InvoiceItemCreate(
    InvoiceItem,
    required_mixin(["title", "quantity", "unitPrice", "relatedInvoice"]),
):
    """
    Pydantic model representing an InvoiceItem

    Note that the tax and gross settings must match those of the invoice
    this item is being attached to, otherwise invoice generation (setting
    `isDraft` to `False`) will fail on EV API side.
    """
