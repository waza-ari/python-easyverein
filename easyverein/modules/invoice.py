import logging
import re
from pathlib import Path
from typing import List
from urllib import parse

from pydantic_core import Url
from requests.structures import CaseInsensitiveDict

from ..core.client import EasyvereinClient
from ..core.exceptions import EasyvereinAPIException
from ..models.invoice import Invoice, InvoiceCreate, InvoiceFilter, InvoiceUpdate
from ..models.invoice_item import InvoiceItemCreate
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

        return self.c.upload(url=self.c.get_url(f"/{self.endpoint_name}/{invoice_id}"), field_name="path", file=file)

    def create_with_attachment(self, invoice: InvoiceCreate, attachment: Path, set_draft_state: bool = True):
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
        if not created_invoice or not created_invoice.id:
            raise EasyvereinAPIException("Failed to create invoice")

        # Upload the attachment
        self.upload_attachment(created_invoice.id, attachment)

        # Set draft state to False if desired
        if set_draft_state:
            self.update(created_invoice.id, InvoiceUpdate(isDraft=False))
            created_invoice.isDraft = False

        return created_invoice

    def create_with_items(
        self,
        invoice: InvoiceCreate,
        items: List[InvoiceItemCreate],
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
        if not inv.id:
            raise EasyvereinAPIException("Failed to create invoice")

        for item in items:
            item.relatedInvoice = inv.id
            self.c.api_instance.invoice_item.create(item)

        if set_draft_state:
            self.update(inv.id, InvoiceUpdate(isDraft=False))
            # We need to fetch new invoice details to obtain the path of the generated PDF
            inv = self.get_by_id(inv.id)

        return inv

    def get_attachment(self, invoice: Invoice | int) -> tuple[bytes, CaseInsensitiveDict[str]]:
        """
        This method downloads and returns the invoice attachment if available.

        It accepts either an invoice object or its id. If the invoice is given, and the path attribute is
        set, it will simply use this path to download and return the file. In all other cases, it first retrieves
        the invoice object by id and then proceeds to download the file.

        Returns a tuple, where the first element is the file and the second contains the headers of the response

        **Usage**

        ```python
        invoice = ev_connection.invoice.get_by_id(invoice_id, query="{id,path}")

        attachment, headers = ev_connection.invoice.get_attachment(invoice)
        ```

        Args:
            invoice: The invoice object or its id for which the attachment should be retrieved
        """
        if isinstance(invoice, Invoice) and invoice.path:
            self.logger.info("Invoice already has the path attribute set, using that path.")
            path = invoice.path
        else:
            self.logger.info("Invoice is either given by id or doesn't contain the path attribute")
            invoice_id = invoice.id if isinstance(invoice, Invoice) else invoice
            if not invoice_id:
                self.logger.error("No invoice id given to retrieve attachment")
                raise EasyvereinAPIException("No invoice id given to retrieve attachment")
            fetched_invoice = self.get_by_id(invoice_id, query="{id,path}")
            if not fetched_invoice or not fetched_invoice.path:
                raise EasyvereinAPIException("No path available for given invoice")
            path = fetched_invoice.path

        if not path or not isinstance(path, Url):
            raise EasyvereinAPIException("Unable to obtain a valid path for given invoice.")

        # Fix for unencoded characters - should probably be fixed in easyverein API
        m = re.fullmatch(r"^(.*\&path=)(.*)(&storedInS3=True)$", path.unicode_string())
        if not m:
            raise EasyvereinAPIException("Unable to parse path for attachment download")
        url_components = list(m.groups())
        if "%" not in url_components[1]:
            url_components[1] = parse.quote(url_components[1])

        return self.c.fetch_file("".join(url_components))
