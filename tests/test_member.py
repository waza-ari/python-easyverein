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

        # Check if all the members are of type Member
        for member in members:
            assert isinstance(member, Member)

    def test_members_with_query(self, ev_connection: EasyvereinAPI):
        query = (
            "{id,membershipNumber,contactDetails{firstName,familyName,privateEmail,_isCompany,companyName},"
            "resignationDate,_isApplication}"
        )

        members = ev_connection.member.get(query=query, limit=2)
        assert len(members) == 2

        for member in members:
            assert isinstance(member, Member)
            print(member)
