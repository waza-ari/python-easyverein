"""
All methods related to invoices
"""
from typing import Union

from ..core.protocol import IsEVClientProtocol
from ..models.invoice import Invoice, InvoiceCreate
from .mixins.recycle_bin import recycle_bin_mixin

recycle_mixin = recycle_bin_mixin("invoice", Invoice)
self_protocol = Union[recycle_mixin, IsEVClientProtocol]


class InvoiceMixin(recycle_mixin):
    """
    All methods related to invoices
    """

    endpoint_name = "invoice"

    def get_invoices(
        self: self_protocol, query: str = None, limit: int = 100
    ) -> list[Invoice]:
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

    def create_invoice(self: self_protocol, invoice: InvoiceCreate) -> Invoice:
        """
        Creates an invoice

        Args:
            invoice (Invoice): Invoice to create
        """
        self.logger.info("Creating invoice %s", invoice.id)

        url = self.c.get_url(f"/{self.endpoint_name}/")

        return self.c.create(url, invoice, Invoice)

    def delete_invoice(
        self: self_protocol,
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

        url = self.c.get_url(f"/{self.endpoint_name}/{invoice.id}/")

        self.c.delete(url)

        if delete_from_recycle_bin:
            self.logger.info("Deleting invoice %s from wastebasket", invoice.id)
            self.purge_invoice(invoice.id)
