import logging
from pathlib import Path
from typing import List

from ..core.client import EasyvereinClient
from ..core.exceptions import EasyvereinAPIException
from ..models.invoice import Invoice, InvoiceCreate, InvoiceFilter, InvoiceUpdate
from ..models.invoice_item import InvoiceItem
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class InvoiceMixin(
    CRUDMixin[Invoice, InvoiceCreate, InvoiceUpdate, InvoiceFilter],
    RecycleBinMixin[Invoice],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "invoice"
        self.return_type = Invoice
        self.c = client
        self.logger = logger

    def upload_attachment(self, invoice: Invoice | int, file: Path):
        """
        Uploads an attachment to an already existing invoice. The invoice must be in draft state, otherwise
        the upload will fail.

        Args:
            invoice: The invoice to upload the attachment to. Can be either an `Invoice` object or its ID
            file: The path to the attachment to be uploaded. Must be a PDF file and a `pathlib.Path` object
        """

        invoice_id = invoice if isinstance(invoice, int) else invoice.id

        return self.c.upload(
            url=self.c.get_url(f"/{self.endpoint_name}/{invoice_id}"),
            field_name="path",
            file=file,
            model=Invoice,
        )

    def create_with_attachment(
        self, invoice: InvoiceCreate, attachment: Path, set_draft_state: bool = True
    ):
        """
        Creates an invoice with an attachment. Note that the only valid file type is PDF.

        Note that this endpoint performs multiple API requests, depending on the final draft
        state. At least two requests are performed (create invoice draft and upload attachment). Then, if
        `set_draft_state` is set to `True` and the models attribute `isDraft` equals `False`, a third request
        is performed afterward to remove the draft state.

        Args:
            invoice: The invoice object to be created
            attachment: The path to the attachment to be uploaded. Must be a PDF file and a `pathlib.Path` object
            set_draft_state: Whether to set the draft state of the invoice to `False` after uploading the attachment
        """

        if not set_draft_state and not invoice.isDraft:
            raise EasyvereinAPIException(
                "Creating an invoice with isDraft set to false is not supported when "
                "we're also instructed not to modify the draft state."
            )

        # Ensure invoice draft state is set to True for now. We'll change it back later
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

        Note that this endpoint performs multiple API requests, depending on the number of items and the final draft
        state. At least, the invoice needs to be created in draft state. Then the items have to be added (one
        API request per item, as the API does not support a bulk create endpoint here). Finally, if
        `set_draft_state` is set to `True` and the models attribute `isDraft` equals `False`, a final request
        is performed afterward to remove the draft state.

        !!! note "PDF generation"
            Starting with the Hexa v1.7 API, the API will automatically generate a PDF attachment based
            on the provided data and the settings configured in the realm settings.

        Args:
            invoice: Invoice to create
            items: List of invoice items to add to the invoice
            set_draft_state: Whether to convert the invoice from draft state to an actual invoice after adding items
        """

        if not set_draft_state and not invoice.isDraft:
            raise EasyvereinAPIException(
                "Creating an invoice with isDraft set to false is not supported when "
                "we're also instructed not to modify the draft state."
            )

        # Set draft to True. If it was false, it will be set back later
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
