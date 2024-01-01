"""
All methods related to invoices
"""
import logging

from ..core.client import EasyvereinClient
from ..models.invoice import Invoice, InvoiceCreate, InvoiceUpdate
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
