"""
All methods related to invoices
"""
import logging
from pathlib import Path
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

    def upload_attachment(self, invoice_id: int, file: Path):
        """
        Uploads an attachment to an invoice
        """
        return self.c.upload(
            url=self.c.get_url(f"/{self.endpoint_name}/{invoice_id}"),
            field_name="path",
            file=file,
            model=Invoice,
        )

    def create_with_attachment(self, invoice: InvoiceCreate, attachment: Path, set_draft_state: bool = True):
        """
        Creates an invoice with an attachment. For invoices, the file must be a PDF.
        """

        if not set_draft_state and not invoice.isDraft:
            raise EasyvereinAPIException(
                "Creating an invoice with isDraft set to false is not supported when "
                "we're also instructed not to modify the draft state."
            )

        # Ensure invoice draft state is set to True for now. We'll change it back later
        old_draft_state = invoice.isDraft
        invoice.isDraft = True

        # Create invoice object
        created_invoice = self.create(invoice)

        # Upload the attachment
        created_invoice = self.upload_attachment(created_invoice.id, attachment)

        # Set draft state to False if desired
        if set_draft_state:
            self.update(created_invoice.id, InvoiceUpdate(isDraft=False))
            created_invoice.isDraft = False

        return created_invoice

    def create_with_items(
        self,
        invoice: InvoiceCreate,
        items: List[InvoiceItem],
        set_draft_state: bool = True,
    ):
        """
        The EV API doesn't support passing the InvoiceItems directly when creating an invoice,
        so this client exposes this helper method to simplify creation of invoices.

        In addition to that, invoices cannot be modified then they're not in the Draft state
        (that is, if `isDraft` is not set to `True`). Therefor this function first creates them
        as draft, then adds the invoice items to the invoice, and optionally updates the
        invoice to remove the draft state, which also triggers the automatic PDF generation
        as of version API version 1.7

        :param invoice: Invoice to create
        :param items: List of invoice items to add to the invoice
        :param set_draft_state: Whether to convert the invoice from draft state to an actual invoice
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

        if set_draft_state:
            self.update(inv.id, InvoiceUpdate(isDraft=False))
            # We need to fetch new invoice details to obtain the path of the generated PDF
            inv = self.get_by_id(inv.id)

        return inv
