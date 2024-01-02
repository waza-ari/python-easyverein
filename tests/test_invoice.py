# content of test_sample.py
import datetime

import pytest
from _pytest.fixtures import FixtureRequest
from pydantic_core import Url

from easyverein import EasyvereinAPI
from easyverein.core.exceptions import EasyvereinAPIException
from easyverein.models.invoice import Invoice, InvoiceCreate, InvoiceUpdate
from easyverein.models.invoice_item import InvoiceItem, InvoiceItemCreate
from easyverein.models.member import Member


class TestInvoices:
    def test_get_invoices(self, ev_connection: EasyvereinAPI):
        invoices = ev_connection.invoice.get()
        # Check if the response is a list
        assert isinstance(invoices, list)

        # We should have 5 invoices based on the example data
        assert len(invoices) == 5

        # Check if all the invoices are of type Invoice
        for invoice in invoices:
            assert isinstance(invoice, Invoice)

    def test_create_invoice_minimal(
        self, ev_connection: EasyvereinAPI, random_string: str
    ):
        # Create a minimal invoice
        invoice_model = InvoiceCreate(
            invNumber=random_string,
            receiver="Test Receiver\nTest Street\n Some weird country",
            totalPrice=100,
        )

        invoice = ev_connection.invoice.create(invoice_model)

        # Check if the response is a list
        assert isinstance(invoice, Invoice)

        # Delete invoice - should now be in recycle bin
        ev_connection.invoice.delete(invoice)

        # Try to create same invoice again, this should yield an error
        with pytest.raises(EasyvereinAPIException):
            ev_connection.invoice.create(invoice_model)

        # Get entries from wastebasket
        deleted_invoices = ev_connection.invoice.get_deleted()
        assert len(deleted_invoices) == 1
        assert deleted_invoices[0].id == invoice.id
        assert deleted_invoices[0].invNumber == invoice.invNumber

        # Finally purge invoice from wastebasket
        ev_connection.invoice.purge(invoice.id)

        # Get entries from wastebasket
        deleted_invoices = ev_connection.invoice.get_deleted()
        assert len(deleted_invoices) == 0

    def test_create_invoice_with_items(
        self, ev_connection: EasyvereinAPI, random_string: str, example_member
    ):
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
        updated_invoice = ev_connection.invoice.update(
            invoice.id, InvoiceUpdate(isDraft=False)
        )
        assert isinstance(updated_invoice, Invoice)
        assert updated_invoice.invNumber == invoice.invNumber
        assert updated_invoice.isDraft is False

        # Delete invoice again
        ev_connection.invoice.delete(invoice, delete_from_recycle_bin=True)
        # Check that we're back to 5 invoices
        invoices = ev_connection.invoice.get_all()
        assert len(invoices) == 5

    def test_create_invoice_with_items_helper(
        self, ev_connection: EasyvereinAPI, random_string: str, example_member
    ):
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

        invoice = ev_connection.invoice.create_with_items(
            invoice_model, invoice_items, True
        )

        # Check if the response is an invoice
        assert isinstance(invoice, Invoice)
        assert invoice.invNumber == invoice_model.invNumber
        assert invoice.isDraft is False
        assert isinstance(invoice.path, Url)

        # Delete invoice again
        ev_connection.invoice.delete(invoice, delete_from_recycle_bin=True)
        # Check that we're back to 5 invoices
        invoices = ev_connection.invoice.get()
        assert len(invoices) == 5

    def test_create_invoice_with_attachment(
        self, ev_connection: EasyvereinAPI, random_string: str, request: FixtureRequest
    ):
        # Get members
        members = ev_connection.member.get()
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

        invoice = ev_connection.invoice.create_with_attachment(
            invoice_model, file, True
        )

        # Check if the response is an invoice
        assert isinstance(invoice, Invoice)
        assert invoice.invNumber == invoice_model.invNumber
        assert invoice.isDraft is False
        assert isinstance(invoice.path, Url)

        # Delete invoice again
        ev_connection.invoice.delete(invoice)
        # Check that we're back to 5 invoices
        invoices = ev_connection.invoice.get()
        assert len(invoices) == 5
