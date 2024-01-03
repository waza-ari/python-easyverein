"""
All methods related to invoices
"""
import logging

from ..core.client import EasyvereinClient
from ..models.invoice_item import InvoiceItem, InvoiceItemCreate, InvoiceItemUpdate
from .mixins.crud import CRUDMixin


class InvoiceItemMixin(CRUDMixin[InvoiceItem, InvoiceItemCreate, InvoiceItemUpdate]):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "invoice-item"
        self.return_type = InvoiceItem
        self.c = client
        self.logger = logger
