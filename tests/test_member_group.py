from easyverein import EasyvereinAPI
from easyverein.models.member_group import MemberGroup, MemberGroupCreate, MemberGroupUpdate


class TestMembeGropr:
    def test_create_member_group_minimal(self, ev_connection: EasyvereinAPI):
        member_group = ev_connection.member_group.create(
            MemberGroupCreate(name="Test-Group", color="#FF0000", short="TG")
        )
        assert isinstance(member_group, MemberGroup)
        assert member_group.name == "Test-Group"
        assert member_group.color == "#FF0000"
        assert member_group.short == "TG"

        # Check some defaults
        assert member_group.taxRate is None
        assert member_group.usePaymentFormula is False
        assert member_group.user_members_groupaccess == "n"
        assert member_group.id

        # Change the color
        mg = ev_connection.member_group.update(member_group.id, MemberGroupUpdate(color="#00FF00"))
        assert isinstance(mg, MemberGroup)

        # Delete member group again
        ev_connection.member_group.delete(member_group)

        # Check waste basket
        member_groups, c = ev_connection.member_group.get_deleted()
        assert isinstance(member_groups, list)
        assert len(member_groups) == 1
        assert c == 1
        assert member_groups[0].id == member_group.id

        # Purge member group
        ev_connection.member_group.purge(member_group)

        # Check waste basket
        member_groups, c = ev_connection.member_group.get_deleted()
        assert isinstance(member_groups, list)
        assert len(member_groups) == 0
        assert c == 0
