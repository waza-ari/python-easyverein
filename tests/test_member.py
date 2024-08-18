import pytest
from easyverein import EasyvereinAPI
from easyverein.core.exceptions import EasyvereinAPINotFoundException
from easyverein.models.member import Member


class TestMember:
    def test_get_members(self, ev_connection: EasyvereinAPI):
        members, total_count = ev_connection.member.get()
        # Check if the response is a list
        assert isinstance(members, list)

        # We should have 5 invoices based on the example data
        assert total_count == 5
        assert len(members) == 5

        # Check if all the members are of type Member
        for member in members:
            assert isinstance(member, Member)

    def test_members_with_query(self, ev_connection: EasyvereinAPI):
        query = (
            "{id,membershipNumber,contactDetails{firstName,familyName,privateEmail,_isCompany,companyName},"
            "resignationDate,_isApplication}"
        )

        members, total_count = ev_connection.member.get(query=query, limit=2)
        assert len(members) == 2
        assert total_count == 5

        for member in members:
            assert isinstance(member, Member)
            assert member.contactDetails.firstName
            assert member.contactDetails.familyName
            assert member.contactDetails.primaryEmail
            assert not member.contactDetails.companyEmail

    def test_member_by_id_not_found(self, ev_connection: EasyvereinAPI):
        # Expect an Exception
        with pytest.raises(EasyvereinAPINotFoundException):
            ev_connection.member.get_by_id(123)
