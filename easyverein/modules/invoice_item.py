"""
All methods related to invoices
"""
import logging

from .mixins.crud import CRUDMixin
from ..core.client import EasyvereinClient
from ..models.invoice_item import InvoiceItem, InvoiceItemCreate, InvoiceItemUpdate


class InvoiceItemMixin(
    CRUDMixin[InvoiceItem, InvoiceItemCreate, InvoiceItemUpdate]
):
    """
    All methods related to invoices
    """

    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "invoice-item"
        self.return_type = InvoiceItem
        self.c = client
        self.logger = logger
