import datetime
from typing import Any

from easyverein import EasyvereinAPI
from easyverein.models.invoice import Invoice, InvoiceFilter
from easyverein.models.member import Member, MemberFilter


class TestFilter:
    @staticmethod
    def validate_response(response: list[Any], model: type, num_expected_results: int):
        """
        Helper method that validates the response of a filter
        """
        # Check if the response is a list
        assert isinstance(response, list)

        # We should have 5 invoices based on the example data
        assert len(response) == num_expected_results

        # Check if all the invoices are of type Invoice
        for instance in response:
            assert isinstance(instance, model)

    def test_filter_invoices(self, ev_connection: EasyvereinAPI):
        search = InvoiceFilter(
            invNumber__in=["1", "3", "5"], canceledInvoice__isnull=True, isDraft=False
        )

        TestFilter.validate_response(
            ev_connection.invoice.get(search=search), Invoice, 3
        )

    def test_filter_members(self, ev_connection: EasyvereinAPI):
        # Case 1: non existing membership number
        search = MemberFilter(membershipNumber="1")
        TestFilter.validate_response(ev_connection.member.get(search=search), Member, 0)

        # Case 2: existing membership number
        search = MemberFilter(membershipNumber="122")
        TestFilter.validate_response(ev_connection.member.get(search=search), Member, 1)

        # Case 3: search by name
        search = MemberFilter(search="Mustermann")
        TestFilter.validate_response(ev_connection.member.get(search=search), Member, 2)

        # Case 4: test bool, get chairmans
        search = MemberFilter(isChairman=True)
        TestFilter.validate_response(ev_connection.member.get(search=search), Member, 5)

        # Case 5: test date, joinDate in future
        search = MemberFilter(joinDate__gte=datetime.datetime.now())
        TestFilter.validate_response(ev_connection.member.get(search=search), Member, 0)

        # Case 6: test date, joinDate in past
        search = MemberFilter(joinDate__lte=datetime.datetime.now())
        TestFilter.validate_response(ev_connection.member.get(search=search), Member, 4)
