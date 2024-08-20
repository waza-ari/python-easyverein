"""
Invoice Item model
"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from ..core.types import EasyVereinReference, FilterIntList
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class InvoiceItemBase(EasyVereinBase):
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
    costCentre: Annotated[str, Field(max_length=8)] | None = None


class InvoiceItem(InvoiceItemBase, EmptyStringsToNone):
    """
    Pydantic model representing an InvoiceItem
    """

    pass


class InvoiceItemCreate(
    InvoiceItemBase,
    required_mixin(["title", "quantity", "unitPrice"]),  # type: ignore
):
    """
    Pydantic model representing an InvoiceItem
    """


class InvoiceItemUpdate(InvoiceItemBase):
    """
    Pydantic model used to patch an InvoiceItem
    """


class InvoiceItemFilter(BaseModel):
    """
    Pydantic model used to filter invoice items
    """

    id__in: FilterIntList | None = None
    title: str | None = None
    taxName: str | None = None
    quantity__gte: int | None = None
    quantity__lte: int | None = None
    description: str | None = None
    billingAccount__isnull: bool | None = None
    relatedInvoice: int | None = None
    relatedInvoice__not: int | None = None
    relatedInvoice__isDraft: bool | None = None
    relatedInvoice__isTemplate: bool | None = None
    billingAccount: str | None = None
    billingAccount__not: str | None = None
    ordering: str | None = None
    search: str | None = None


from .invoice import Invoice  # noqa: E402
