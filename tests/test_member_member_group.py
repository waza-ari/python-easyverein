import pytest
from easyverein import EasyvereinAPI, EasyvereinAPIException
from easyverein.models import Member, MemberGroup, MemberGroupCreate, MemberMemberGroup
from pydantic_core import Url


@pytest.fixture(scope="class")
def group(ev_connection: EasyvereinAPI):
    member_group = ev_connection.member_group.create(MemberGroupCreate(name="Test-Group", color="#FF0000", short="TG"))
    yield member_group
    ev_connection.member_group.delete(member_group, delete_from_recycle_bin=True)


class TestMemberMemberGroup:
    def test_create_group_association(self, ev_connection: EasyvereinAPI, example_member: Member, group: MemberGroup):
        assert example_member.id

        # Check that the member currently is not in the group
        assert ev_connection.member.member_group(example_member.id).get_group_membership(group) is None

        # Add the member to the group
        ev_connection.member.member_group(example_member.id).add_to_group(group)

        # Check that the member now is in the group
        assert ev_connection.member.member_group(example_member.id).get_group_membership(group) is not None

        # Remove the member from the group
        ev_connection.member.member_group(example_member.id).remove_from_group(group)

        # Check that the member currently is not in the group
        assert ev_connection.member.member_group(example_member.id).get_group_membership(group) is None

    def test_billing_active_state(self, ev_connection: EasyvereinAPI, example_member: Member, group: MemberGroup):
        assert example_member.id
        assert group.id

        # Add them to the group
        group_membership = ev_connection.member.member_group(example_member.id).add_to_group(group)
        assert isinstance(group_membership, MemberMemberGroup)
        assert isinstance(group_membership.userObject, Url)
        assert isinstance(group_membership.memberGroup, Url)
        assert str(group_membership.userObject).endswith(str(example_member.id))
        assert str(group_membership.memberGroup).endswith(str(group.id))
        assert group_membership.id

        # Billing is not active by default
        assert not group_membership.paymentActive

        # Activate billing
        ev_connection.member.member_group(example_member.id).set_group_billing_status(group, True)

        # Fetch the group membership again
        group_membership = ev_connection.member.member_group(example_member.id).get_group_membership(group)
        assert group_membership is not None
        assert isinstance(group_membership.userObject, Url)
        assert isinstance(group_membership.memberGroup, Url)
        assert str(group_membership.userObject).endswith(str(example_member.id))
        assert str(group_membership.memberGroup).endswith(str(group.id))
        assert group_membership.id
        assert group_membership.paymentActive

        # Remove the member from the group
        ev_connection.member.member_group(example_member.id).remove_from_group(group)

    def test_without_helper(self, ev_connection: EasyvereinAPI, example_member, group: MemberGroup):
        assert example_member.id
        assert group.id

        # Add the member to the group
        group_membership = ev_connection.member.member_group(example_member.id).create(
            MemberMemberGroup(userObject=example_member.id, memberGroup=group.id)
        )
        assert isinstance(group_membership, MemberMemberGroup)
        assert isinstance(group_membership.userObject, Url)
        assert isinstance(group_membership.memberGroup, Url)
        assert str(group_membership.userObject).endswith(str(example_member.id))
        assert str(group_membership.memberGroup).endswith(str(group.id))
        assert group_membership.id

        # Check that the member now is in the group
        assert ev_connection.member.member_group(example_member.id).get_group_membership(group) is not None

        # Remove the member from the group
        ev_connection.member.member_group(example_member.id).delete(group_membership)

        # Check that the member currently is not in the group
        assert ev_connection.member.member_group(example_member.id).get_group_membership(group) is None

    def test_ignore_existing(self, ev_connection: EasyvereinAPI, example_member: Member, group: MemberGroup):
        assert example_member.id
        assert group.id

        # Add the member to the group
        group_membership = ev_connection.member.member_group(example_member.id).add_to_group(group)
        assert isinstance(group_membership, MemberMemberGroup)
        assert isinstance(group_membership.userObject, Url)
        assert isinstance(group_membership.memberGroup, Url)
        assert str(group_membership.userObject).endswith(str(example_member.id))
        assert str(group_membership.memberGroup).endswith(str(group.id))
        assert group_membership.id

        # Add the member to the group again
        group_membership = ev_connection.member.member_group(example_member.id).add_to_group(
            group, ignore_existing=True
        )
        assert group_membership is None

        # Add the member to the group again, but this time raise an exception
        with pytest.raises(EasyvereinAPIException):
            ev_connection.member.member_group(example_member.id).add_to_group(group, ignore_existing=False)

        # Remove the member from the group
        ev_connection.member.member_group(example_member.id).remove_from_group(group)

    def test_remove_non_existing(self, ev_connection: EasyvereinAPI, example_member: Member, group: MemberGroup):
        assert example_member.id
        assert group.id

        # Remove the member from the group
        with pytest.raises(EasyvereinAPIException):
            ev_connection.member.member_group(example_member.id).remove_from_group(group)

    def test_remove_non_existing_group(self, ev_connection: EasyvereinAPI, example_member: Member):
        assert example_member.id

        # Remove the member from the group
        with pytest.raises(EasyvereinAPIException):
            ev_connection.member.member_group(example_member.id).remove_from_group(999999)

    def test_add_non_existing_group(self, ev_connection: EasyvereinAPI, example_member: Member):
        assert example_member.id

        # Add the member to the group
        with pytest.raises(EasyvereinAPIException):
            ev_connection.member.member_group(example_member.id).add_to_group(999999)
