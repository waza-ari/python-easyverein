from easyverein import EasyvereinAPI
from easyverein.models.invoice import Invoice, InvoiceFilter


class TestFilter:
    def test_filter_invoices(self, ev_connection: EasyvereinAPI):
        search = InvoiceFilter(
            invNumber__in=["1", "3", "5"], canceledInvoice__isnull=True, isDraft=False
        )

        invoices = ev_connection.invoice.get(search=search)

        # Check if the response is a list
        assert isinstance(invoices, list)

        # We should have 5 invoices based on the example data
        assert len(invoices) == 3

        # Check if all the invoices are of type Invoice
        for invoice in invoices:
            assert isinstance(invoice, Invoice)
