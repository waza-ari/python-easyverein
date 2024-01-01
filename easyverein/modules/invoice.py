"""
All methods related to invoices
"""
import logging

from ..core.client import EasyvereinClient
from ..models.invoice import Invoice, InvoiceCreate, InvoiceUpdate
from .mixins.recycle_bin import recycle_bin_mixin

recycle_mixin = recycle_bin_mixin(Invoice)


class InvoiceMixin(recycle_mixin):
    """
    All methods related to invoices
    """

    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "invoice"
        self.c = client
        self.logger = logger

    def get(self, query: str = None, limit: int = 100) -> list[Invoice]:
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

        return self.c.fetch_paginated(url, Invoice, limit)

    def get_by_id(self, invoice_id: int) -> Invoice:
        """
        Fetches an invoice from the API

        Args:
            invoice_id (int): ID of the invoice
        """
        self.logger.info("Fetching invoice %s from API", invoice_id)

        url = self.c.get_url(f"/{self.endpoint_name}/{invoice_id}")

        return self.c.fetch_one(url, Invoice)

    def create(self, invoice: InvoiceCreate) -> Invoice:
        """
        Creates an invoice

        Args:
            invoice (Invoice): Invoice to create
        """
        self.logger.info("Creating invoice %s", invoice.invNumber)

        url = self.c.get_url(f"/{self.endpoint_name}/")

        return self.c.create(url, invoice, Invoice)

    def update(self, invoice_id: int, invoice: InvoiceUpdate) -> Invoice:
        """
        Updates an invoice

        Args:
            invoice_id (int): ID of the invoice to update
            invoice (InvoiceUpdate): Update model
        """
        self.logger.info("Updating invoice %s", invoice_id)

        url = self.c.get_url(f"/{self.endpoint_name}/{invoice_id}")

        return self.c.update(url, invoice, Invoice)

    def delete(
        self,
        invoice: Invoice,
        delete_from_recycle_bin: bool = False,
    ):
        """
        Deletes an invoice

        Args:
            invoice (Invoice): Invoice to delete
            delete_from_recycle_bin (bool, optional): Whether to delete the invoice
                also from the recycle bin. Defaults to False.
        """
        self.logger.info("Deleting invoice %s", invoice.id)

        url = self.c.get_url(f"/{self.endpoint_name}/{invoice.id}")

        self.c.delete(url)

        if delete_from_recycle_bin:
            self.logger.info("Deleting invoice %s from wastebasket", invoice.id)
            self.purge(invoice.id)
