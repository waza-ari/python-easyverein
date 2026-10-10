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
from .mixins.crud import BulkUpdateCreateMixin, CRUDMixin
from .mixins.helper import parse_models
from .mixins.recycle_bin import RecycleBinMixin


class InvoiceMixin(
    CRUDMixin[Invoice, InvoiceCreate, InvoiceUpdate, InvoiceFilter],
    BulkUpdateCreateMixin[Invoice, InvoiceCreate, InvoiceUpdate],
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
    ) -> Invoice:
        """
        Creates an invoice together with its invoice items in a single API request and returns the created invoice.

        The request is atomic: if the invoice or any of the items fails validation, the API returns an error
        and nothing is created. The `relatedInvoice` attribute of the items is ignored, as the items are
        attached to the newly created invoice.

        !!! note "PDF generation"
            If the invoice is not created as a draft, the API automatically generates the PDF based on the
            provided data and the settings configured in the organization. The returned invoice contains
            its `path` already.

        Args:
            invoice: Invoice to create
            items: List of invoice items to add to the invoice
            set_draft_state: If `True` (default), the invoice is created as final invoice (`isDraft=False`),
                otherwise it is created as draft. Passing `False` requires `invoice.isDraft` to be `True`.
        """

        if not set_draft_state and not invoice.isDraft:
            raise EasyvereinAPIException(
                "Creating an invoice with isDraft set to false is not supported when "
                "we're also instructed not to modify the draft state."
            )

        api_version = self.c.api_version
        related_invoice_key = InvoiceItemCreate.wire_name("relatedInvoice", api_version)
        items_key = InvoiceCreate.wire_name("invoiceItems", api_version)
        assert related_invoice_key and items_key

        payload = self.c.serialize(invoice.model_copy(update={"isDraft": not set_draft_state}))
        payload[items_key] = [
            {k: v for k, v in self.c.serialize(item).items() if k != related_invoice_key} for item in items
        ]

        self.logger.info(f"Creating object of type {self.endpoint_name} with {len(items)} items")
        response = self.c.create(self.c.get_url(f"/{self.endpoint_name}/create-invoice"), payload)
        assert isinstance(response.result, dict)
        return parse_models(response.result, Invoice, self.c.context)

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
