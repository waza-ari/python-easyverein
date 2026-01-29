from datetime import date, datetime, timedelta
from typing import Generator

import pytest
from easyverein import EasyvereinAPI
from easyverein.core.exceptions import EasyvereinAPINotFoundException
from easyverein.models.contact_details import ContactDetails, ContactDetailsCreate
from easyverein.models.member import Member, MemberCreate, MemberSetDosb, MemberSetLsb, MemberUpdate


@pytest.fixture(scope="module", autouse=True)
def _remove_test_members_and_cas(ev_connection: EasyvereinAPI) -> Generator[None, None, None]:
    yield

    for m in ev_connection.member.get_all(query="{id,contactDetails{firstName,id}}"):
        if not isinstance(m.contactDetails.firstName, str) and m.contactDetails.firstName.lower().startswith("test_"):  # type: ignore
            ev_connection.member.delete(m, delete_from_recycle_bin=True)
            ev_connection.contact_details.delete(m.contactDetails, delete_from_recycle_bin=True)  # type: ignore


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

    def test_related_members(self, ev_connection: EasyvereinAPI):
        # Get all members
        members, total_count = ev_connection.member.get()
        assert total_count == 5
        assert len(members) == 5

        # Update member
        owner_member = members[0]
        assert isinstance(owner_member, Member)
        related_member = members[1]
        assert isinstance(related_member, Member)
        ev_connection.member.update(target=owner_member, data=MemberUpdate(relatedMembers=[related_member.id]))

        # Get updated member
        assert isinstance(owner_member.id, int)
        updated_member = ev_connection.member.get_by_id(owner_member.id, query="{id,relatedMembers{id}}")
        assert isinstance(updated_member, Member)
        assert updated_member.relatedMembers is not None
        assert isinstance(updated_member.relatedMembers, list)
        assert isinstance(updated_member.relatedMembers[0], Member)
        assert related_member.id in [m.id for m in updated_member.relatedMembers]

        # Reset
        ev_connection.member.update(target=owner_member, data=MemberUpdate(relatedMembers=[]))
        assert isinstance(owner_member.id, int)
        reset_member = ev_connection.member.get_by_id(owner_member.id, query="{id,relatedMembers{id}}")
        assert isinstance(reset_member, Member)
        assert isinstance(reset_member.relatedMembers, list)
        assert reset_member.relatedMembers == []


class TestMemberSetLsb:
    def test_set_lsb(self, ev_connection: EasyvereinAPI, example_member: Member):
        assert example_member.id

        # Set a LSB sport
        ev_connection.member.set_lsb(example_member.id, MemberSetLsb(lsbSport=["1"]))

        # Verify
        member = ev_connection.member.get_by_id(example_member.id, query="{id,integrationLsbSport{id}}")
        assert member.integrationLsbSport is not None
        assert len(member.integrationLsbSport) > 0

        # Unset it again
        ev_connection.member.set_lsb(example_member.id, MemberSetLsb(lsbSport=[]))

        # Verify
        member = ev_connection.member.get_by_id(example_member.id, query="{id,integrationLsbSport{id}}")
        assert member.integrationLsbSport == []


class TestMemberSetDosb:
    def test_set_dosb(self, ev_connection: EasyvereinAPI, example_member: Member):
        assert example_member.id

        # Set a DOSB sport
        ev_connection.member.set_dosb(example_member.id, MemberSetDosb(dosb_sport=["1"]))

        # Verify
        member = ev_connection.member.get_by_id(example_member.id, query="{id,integrationDosbSport{id}}")
        assert member.integrationDosbSport is not None
        assert len(member.integrationDosbSport) > 0

        # Unset
        ev_connection.member.set_dosb(example_member.id, MemberSetDosb(dosb_sport=[]))

        # Verify
        member = ev_connection.member.get_by_id(example_member.id, query="{id,integrationDosbSport{id}}")
        assert member.integrationDosbSport == []


class TestMemberBulk:
    def test_bulk_create(self, ev_connection: EasyvereinAPI, example_member: Member, random_string: str):
        name = random_string
        ev_connection.contact_details.bulk_create(
            [
                ContactDetailsCreate(firstName=f"test_{name}1", familyName="Member", isCompany=False),
                ContactDetailsCreate(firstName=f"test_{name}2", familyName="Member", isCompany=False),
            ]
        )
        cds = [
            c
            for c in ev_connection.contact_details.get_all(query="{id,firstName}")
            if c.firstName and c.firstName.startswith(f"test_{name}")
        ]

        member_data = [
            MemberCreate(emailOrUserName=f"test_{name}1@example.com", contactDetails=cds[0].id),
            MemberCreate(emailOrUserName=f"test_{name}2@example.com", contactDetails=cds[1].id),
        ]

        successes = ev_connection.member.bulk_create(member_data)
        assert successes == [True, True]

        created_members = [
            m
            for m in ev_connection.member.get_all(query="{id,contactDetails{firstName}}")
            if m.contactDetails.firstName and m.contactDetails.firstName.startswith(f"test_{name}")  # type: ignore
        ]

        assert isinstance(created_members, list)
        assert len(created_members) == 2

    def test_bulk_update(self, ev_connection: EasyvereinAPI):
        members = ev_connection.member.get_all(query="{id,joinDate}")[:2]

        dates_before: list[datetime | None] = [m.joinDate for m in members]
        dates_after = [d + timedelta(days=1) if d else date(1970, 1, 1) for d in dates_before]

        update_data = [MemberUpdate(id=m.id, joinDate=d) for m, d in zip(members, dates_after)]

        ev_connection.member.bulk_update(update_data)

        updated_members = ev_connection.member.get_all(query="{id,joinDate}")[:2]

        assert isinstance(updated_members, list)
        assert len(updated_members) == 2
        assert [m.joinDate for m in updated_members] == dates_after

        # reset data
        ev_connection.member.bulk_update(
            [MemberUpdate(id=m.id, joinDate=d) for m, d in zip(members, dates_before)], exclude_none=False
        )
        reset_members = ev_connection.member.get_all(query="{id,joinDate}")[:2]
        assert [m.joinDate for m in reset_members] == dates_before
