"""
All methods related to invoices
"""
import logging

from ..core.client import EasyvereinClient
from ..models.invoice_item import InvoiceItem, InvoiceItemCreate


class InvoiceItemMixin:
    """
    All methods related to invoices
    """

    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "invoice-item"
        self.c = client
        self.logger = logger

    def get(self, query: str = None, limit: int = 100) -> list[InvoiceItem]:
        """
        Fetches all invoices from the API

        Args:
            query (str, optional): Query to use with API. Defaults to None.
            limit (int, optional): How many resources per request. Defaults to 100.
        """
        self.logger.info("Fetching all invoices from API")

        url = self.c.get_url(
            f"/{self.endpoint_name}/" + (("?query=" + query) if query else "")
        )

        return self.c.fetch_paginated(url, InvoiceItem, limit)

    def get_by_id(self, invoice_item_id: int) -> InvoiceItem:
        """
        Fetches an invoice item from the API

        Args:
            invoice_item_id (int): ID of the invoice
        """
        self.logger.info("Fetching invoice %s from API", invoice_item_id)

        url = self.c.get_url(f"/{self.endpoint_name}/{invoice_item_id}")

        return self.c.fetch_one(url, InvoiceItem)

    def create(self, invoice_item: InvoiceItemCreate) -> InvoiceItem:
        """
        Creates an invoice

        Args:
            invoice_item (InvoiceItem): Invoice item to create. Must be attached to an existing invoice
        """
        self.logger.info("Creating invoice item %s", invoice_item.title)

        url = self.c.get_url(f"/{self.endpoint_name}/")

        return self.c.create(url, invoice_item, InvoiceItem)

    def delete(
        self,
        invoice_item: InvoiceItem,
    ):
        """
        Deletes an invoiceItem

        Args:
            invoice_item (Invoice): InvoiceItem to delete
        """
        self.logger.info("Deleting invoice %s", invoice_item.id)

        url = self.c.get_url(f"/{self.endpoint_name}/{invoice_item.id}")

        self.c.delete(url)
