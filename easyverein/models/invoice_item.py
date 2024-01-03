"""
Invoice Item model
"""
from __future__ import annotations

from typing import Annotated

from pydantic import PositiveInt, StringConstraints

from ..core.types import EasyVereinReference
from .base import EasyVereinBase
from .mixins.required_attributes import required_mixin


class InvoiceItem(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `InvoiceItem` | `InvoiceUpdateItem` | `InvoiceItemCreate` |

    !!! tip "Creating Invoice Items"
        Invoice Items can only be created once the invoice is already created and is still in the draft state.
        Also note that the tax and gross settings must match those of the invoice this item is being attached to,
        otherwise invoice generation (setting `isDraft` to `False`) will fail on EV API side.
    """

    relatedInvoice: Invoice | EasyVereinReference | None = None
    quantity: PositiveInt | None = None
    unitPrice: float | None = None
    totalPrice: float | None = None
    title: str | None = None
    description: str | None = None
    taxRate: float | None = None
    gross: bool | None = None
    taxName: str | None = None
    # TODO: Add reference to BillingAccount once implemented
    billingAccount: EasyVereinReference | None = None
    costCentre: Annotated[str, StringConstraints(max_length=8)] | None = None


class InvoiceItemCreate(
    InvoiceItem,
    required_mixin(["title", "quantity", "unitPrice"]),
):
    """
    Pydantic model representing an InvoiceItem
    """


class InvoiceItemUpdate(InvoiceItem):
    """
    Pydantic model used to patch an InvoiceItem
    """


from .invoice import Invoice  # noqa: E402
