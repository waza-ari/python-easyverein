import datetime

import pytest
from _pytest.fixtures import FixtureRequest
from easyverein import EasyvereinAPI
from easyverein.core.exceptions import EasyvereinAPIException
from easyverein.models.invoice import Invoice, InvoiceCreate, InvoiceUpdate
from easyverein.models.invoice_item import InvoiceItem, InvoiceItemCreate
from easyverein.models.member import Member
from pydantic_core import Url
from requests.structures import CaseInsensitiveDict


class TestInvoices:
    def test_get_invoices(self, ev_connection: EasyvereinAPI):
        invoices, total_count = ev_connection.invoice.get()
        # Check if the response is a list
        assert isinstance(invoices, list)

        # We should have 6 invoices based on the example data
        # 4 regular invoices, 2 requests
        assert total_count == 6
        assert len(invoices) == 6

        # Check if all the invoices are of type Invoice
        for invoice in invoices:
            assert isinstance(invoice, Invoice)

    def test_get_attachment(self, ev_connection: EasyvereinAPI):
        invoices, _ = ev_connection.invoice.get()
        invoice = invoices[0]
        assert isinstance(invoice, Invoice)
        assert isinstance(invoice.id, int)

        # Get attachment using the pre-populated invoice object
        attachment, headers = ev_connection.invoice.get_attachment(invoice)

        assert isinstance(headers, CaseInsensitiveDict)
        assert isinstance(attachment, bytes)

        # Get attachment again by ID only
        attachment2, headers2 = ev_connection.invoice.get_attachment(invoice.id)

        assert isinstance(headers2, CaseInsensitiveDict)
        assert isinstance(attachment2, bytes)

        # Should have same length
        assert len(attachment) == len(attachment2)

        # Verify header contains Content-Type (that key is in dict)
        assert "Content-Type" in headers
        assert "Content-Type" in headers2

        # Verify header contains same Content-Type
        assert headers["Content-Type"] == "application/pdf;charset=utf-8"
        assert headers2["Content-Type"] == "application/pdf;charset=utf-8"

        # Verify headers contain Content Disposition
        assert "Content-Disposition" in headers
        assert "Content-Disposition" in headers2

        # Verify headers contain same Content Disposition
        assert headers["Content-Disposition"] == headers2["Content-Disposition"]

        # Verify it contains the keyword attachmet and a filename
        assert "attachment" in headers["Content-Disposition"]
        assert headers["Content-Disposition"].split(";")[1].strip().startswith("filename=")

        # Verify header content length matches actual length
        assert len(attachment) == int(headers["Content-Length"])
        assert len(attachment2) == int(headers2["Content-Length"])

    def test_create_invoice_minimal(self, ev_connection: EasyvereinAPI, random_string: str):
        # Create a minimal invoice
        invoice_model = InvoiceCreate(
            invNumber=random_string,
            receiver="Test Receiver\nTest Street\n Some weird country",
            totalPrice=100,
        )

        invoice = ev_connection.invoice.create(invoice_model)

        # Check if the response is a list
        assert isinstance(invoice, Invoice)
        assert isinstance(invoice.id, int)

        # Delete invoice - should now be in recycle bin
        ev_connection.invoice.delete(invoice)

        # Try to create same invoice again, this should yield an error
        with pytest.raises(EasyvereinAPIException):
            ev_connection.invoice.create(invoice_model)

        # Get entries from wastebasket
        deleted_invoices, _ = ev_connection.invoice.get_deleted()
        assert len(deleted_invoices) == 1
        assert deleted_invoices[0].id == invoice.id
        assert deleted_invoices[0].invNumber == invoice.invNumber

        # Finally purge invoice from wastebasket
        ev_connection.invoice.purge(invoice.id)

        # Get entries from wastebasket
        deleted_invoices, _ = ev_connection.invoice.get_deleted()
        assert len(deleted_invoices) == 0

    def test_create_invoice_with_items(self, ev_connection: EasyvereinAPI, random_string: str, example_member):
        # Create a minimal invoice
        invoice_model = InvoiceCreate(
            invNumber=random_string,
            totalPrice=50.60,
            date=datetime.date.today(),
            dateItHappend=datetime.date.today(),
            isDraft=True,
            gross=True,
            description="Test Description",
            kind="revenue",
            isTemplate=False,
            isRequest=False,
            paymentInformation="debit",
            taxRate=0.00,
            relatedAddress=example_member.contactDetails,
            payedFromUser=example_member.id,
            storedInS3=False,
        )

        invoice = ev_connection.invoice.create(invoice_model)

        # Check if the response is an invoice
        assert isinstance(invoice, Invoice)
        assert invoice.invNumber == invoice_model.invNumber
        assert invoice.isDraft
        assert isinstance(invoice.id, int)

        # Create an invoice item
        invoice_item_model = InvoiceItemCreate(
            title="Test Invoice Item",
            quantity=5,
            unitPrice=10.12,
            relatedInvoice=invoice.id,
            taxRate=0,
            gross=True,
        )

        invoice_item = ev_connection.invoice_item.create(invoice_item_model)

        # Check that the item was created
        assert isinstance(invoice_item, InvoiceItem)

        # Convert invoice to non-draft
        updated_invoice = ev_connection.invoice.update(invoice.id, InvoiceUpdate(isDraft=False))
        assert isinstance(updated_invoice, Invoice)
        assert updated_invoice.invNumber == invoice.invNumber
        assert updated_invoice.isDraft is False

        # Delete invoice again
        ev_connection.invoice.delete(invoice, delete_from_recycle_bin=True)
        # Check that we're back to 6 invoices
        invoices = ev_connection.invoice.get_all()
        assert len(invoices) == 6

    def test_create_invoice_with_items_helper(self, ev_connection: EasyvereinAPI, random_string: str, example_member):
        # Create a minimal invoice
        invoice_model = InvoiceCreate(
            invNumber=random_string,
            totalPrice=102.90,
            date=datetime.date.today(),
            dateItHappend=datetime.date.today(),
            isDraft=False,
            gross=True,
            description="Test Description",
            kind="revenue",
            isTemplate=False,
            isRequest=False,
            paymentInformation="debit",
            taxRate=0.00,
            relatedAddress=example_member.contactDetails,
            payedFromUser=example_member.id,
            storedInS3=False,
        )

        # Create two invoice item
        invoice_items = [
            InvoiceItemCreate(
                title="First Invoice Item",
                quantity=5,
                unitPrice=10.12,
                taxRate=0,
                gross=True,
            ),
            InvoiceItemCreate(
                title="Second Invoice Item",
                quantity=10,
                unitPrice=5.23,
                taxRate=0,
                gross=True,
            ),
        ]

        invoice = ev_connection.invoice.create_with_items(invoice_model, invoice_items, True)

        # Check if the response is an invoice
        assert isinstance(invoice, Invoice)
        assert invoice.invNumber == invoice_model.invNumber
        assert invoice.isDraft is False
        assert isinstance(invoice.path, Url)

        # Delete invoice again
        ev_connection.invoice.delete(invoice, delete_from_recycle_bin=True)
        # Check that we're back to 6 invoices
        invoices, total_count = ev_connection.invoice.get()
        assert total_count == 6
        assert len(invoices) == 6

    def test_create_invoice_with_attachment(
        self, ev_connection: EasyvereinAPI, random_string: str, request: FixtureRequest
    ):
        # Get members
        members, _ = ev_connection.member.get()
        assert len(members) > 0
        member = members[1]

        assert isinstance(member, Member)

        # Create a minimal invoice
        invoice_model = InvoiceCreate(
            invNumber=random_string,
            totalPrice=21.10,
            date=datetime.date.today(),
            dateItHappend=datetime.date.today() - datetime.timedelta(days=30),
            isDraft=False,
            gross=True,
            description="Test Attachment Upload",
            isRequest=True,
            taxRate=0.00,
            relatedAddress=member.contactDetails,
            payedFromUser=member.id,
        )

        file = request.path.parent / "data" / "dummy.pdf"

        invoice = ev_connection.invoice.create_with_attachment(invoice_model, file, True)

        # Check if the response is an invoice
        assert isinstance(invoice, Invoice)
        assert invoice.invNumber == invoice_model.invNumber
        assert invoice.isDraft is False

        # Delete invoice again
        ev_connection.invoice.delete(invoice)

        # Check that we're back to 6 invoices
        invoices, _ = ev_connection.invoice.get()
        assert len(invoices) == 6

        # Purge invoice from wastebasket
        assert invoice.id is not None
        ev_connection.invoice.purge(invoice.id)
