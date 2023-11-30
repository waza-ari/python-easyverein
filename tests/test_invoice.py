# content of test_sample.py
import pytest

from easyverein import EasyvereinAPI
from easyverein.core.exceptions import EasyvereinAPIException
from easyverein.models.invoice import Invoice, InvoiceCreate


class TestInvoices:
    def test_get_invoices(self, ev_connection: EasyvereinAPI):
        invoices = ev_connection.get_invoices()
        # Check if the response is a list
        assert isinstance(invoices, list)

        # We should have 5 invoices based on the example data
        assert len(invoices) == 5

        # Check if all the invoices are of type Invoice
        for invoice in invoices:
            assert isinstance(invoice, Invoice)

    def test_create_invoice_minimal(self, ev_connection: EasyvereinAPI):
        # Create a minimal invoice
        invoice_model = InvoiceCreate(
            invNumber="Test-Invoice-1",
            receiver="Test Receiver\nTest Street\n Some weird country",
            totalPrice=100,
        )

        invoice = ev_connection.create_invoice(invoice_model)

        # Check if the response is a list
        assert isinstance(invoice, Invoice)

        # Delete invoice - should now be in recycle bin
        ev_connection.delete_invoice(invoice)

        # Try to create same invoice again, this should yield an error
        with pytest.raises(EasyvereinAPIException):
            ev_connection.create_invoice(invoice_model)

        # Get entries from wastebasket
        deleted_invoices = ev_connection.get_deleted_invoices()
        assert len(deleted_invoices) == 1
        assert deleted_invoices[0].id == invoice.id
        assert deleted_invoices[0].invNumber == invoice.invNumber

        # Finally purge invoice from wastebasket
        ev_connection.purge_invoice(invoice.id)

        # Get entries from wastebasket
        deleted_invoices = ev_connection.get_deleted_invoices()
        assert len(deleted_invoices) == 0
