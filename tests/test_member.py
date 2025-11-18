import pytest
from easyverein import EasyvereinAPI
from easyverein.core.exceptions import EasyvereinAPINotFoundException
from easyverein.models.contact_details import ContactDetails
from easyverein.models.member import Member, MemberFilter, MemberUpdate


class TestMember:
    def test_get_members(self, ev_connection: EasyvereinAPI):
        members, total_count = ev_connection.member.get()
        # Check if the response is a list
        assert isinstance(members, list)

        # We should have 5 members based on the example data
        # 4 regular members, 1 requests
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
            assert isinstance(member.contactDetails, ContactDetails)
            if member.contactDetails.isCompany:
                assert member.contactDetails.companyName
                assert member.contactDetails.primaryEmail
            else:
                assert member.contactDetails.firstName
                assert member.contactDetails.familyName
                assert not member.contactDetails.companyEmail

    def test_member_by_id_not_found(self, ev_connection: EasyvereinAPI):
        # Expect an Exception
        with pytest.raises(EasyvereinAPINotFoundException):
            ev_connection.member.get_by_id(123)

    def test_member_with_filter(self, ev_connection: EasyvereinAPI):
        members, total_count = ev_connection.member.get(search=MemberFilter(isChairman=False))
        assert len(members) == 4
        assert total_count == 4

    def test_related_members(self, ev_connection: EasyvereinAPI):
        member = ev_connection.member.get_by_id(4187730)

        ev_connection.member.update(target=member.id, data=MemberUpdate(relatedMembers=[4187733]))

        updated_member = ev_connection.member.get_by_id(4187730, query="{id,relatedMembers{id}}")

        assert updated_member.relatedMembers is not None
        assert 4187733 in [m.id for m in updated_member.relatedMembers]

        # reset
        ev_connection.member.update(target=member.id, data=MemberUpdate(relatedMembers=[]))
        reset_member = ev_connection.member.get_by_id(4187730, query="{id,relatedMembers{id}}")
        assert reset_member.relatedMembers is None
