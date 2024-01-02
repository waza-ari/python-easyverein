"""
All methods related to invoices
"""
import logging
from typing import List

from ..core.client import EasyvereinClient
from ..core.exceptions import EasyvereinAPIException
from ..models.invoice import Invoice, InvoiceCreate, InvoiceUpdate
from ..models.invoice_item import InvoiceItem
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class InvoiceMixin(
    CRUDMixin[Invoice, InvoiceCreate, InvoiceUpdate], RecycleBinMixin[Invoice]
):
    """
    All methods related to invoices
    """

    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "invoice"
        self.return_type = Invoice
        self.c = client
        self.logger = logger

    def create_with_items(
        self,
        invoice: InvoiceCreate,
        items: List[InvoiceItem],
        set_draft_state: bool = False,
    ):
        """
        The EV API doesn't support passing the InvoiceItems directly when creating an invoice,
        so this client exposes this helper method to simplify creation of invoices.

        In addition to that, invoices cannot be modified then they're not in the Draft state
        (that is, if `isDraft` is not set to `True`). Therefor this function first creates them
        as draft, then adds the invoice items to the invoice, and optionally updates the
        invoice to remove the draft state, which also triggers the automatic PDF generation
        as of version API version 1.7
        """

        if not set_draft_state and not invoice.isDraft:
            raise EasyvereinAPIException(
                "Creating an invoice with isDraft set to false is not supported when "
                "we're also instructed not to modify the draft state."
            )

        old_draft_state = invoice.isDraft
        invoice.isDraft = True

        inv = self.create(invoice)
        for item in items:
            item.relatedInvoice = inv.id
            self.c.api_instance.invoice_item.create(item)

        if not old_draft_state:
            self.update(inv.id, InvoiceUpdate(isDraft=False))
            # We need to fetch new invoice details to obtain the path of the generated PDF
            inv = self.get_by_id(inv.id)

        return inv
