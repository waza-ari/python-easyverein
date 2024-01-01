# content of test_sample.py

from easyverein import EasyvereinAPI
from easyverein.models.member import Member


class TestMember:
    def test_get_members(self, ev_connection: EasyvereinAPI):
        members = ev_connection.member.get()
        # Check if the response is a list
        assert isinstance(members, list)

        # We should have 5 invoices based on the example data
        assert len(members) == 5

        # Check if all the invoices are of type Invoice
        for member in members:
            assert isinstance(member, Member)
