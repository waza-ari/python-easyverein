import pytest
from easyverein import EasyvereinAPI
from easyverein.models import (
    MemberCustomField,
    MemberCustomFieldCreate,
    MemberCustomFieldUpdate,
)


@pytest.fixture(scope="class")
def example_member_custom_field(ev_connection: EasyvereinAPI, example_member, example_custom_field):
    member_custom_field = ev_connection.member.custom_field(example_member.id).create(
        MemberCustomFieldCreate(customField=example_custom_field.id, value="Example-Value"),
    )
    yield member_custom_field
    ev_connection.member.custom_field(example_member.id).delete(member_custom_field)


class TestMemberCustomField:
    def test_create_custom_field(self, ev_connection: EasyvereinAPI, example_member, example_custom_field):
        member_custom_field = ev_connection.member.custom_field(example_member.id).create(
            MemberCustomFieldCreate(customField=example_custom_field.id, value="Example-Value")
        )
        assert isinstance(member_custom_field, MemberCustomField)
        assert member_custom_field.value == "Example-Value"

        # Delete it again
        ev_connection.member.custom_field(example_member.id).delete(member_custom_field)

    def test_modify_custom_field(self, ev_connection: EasyvereinAPI, example_member_custom_field, example_member):
        member_custom_field = ev_connection.member.custom_field(example_member.id).update(
            example_member_custom_field.id, MemberCustomFieldUpdate(value="Modified-Value")
        )

        # Check that the value was modified
        assert member_custom_field.value == "Modified-Value"

    def test_ensure_custom_field_value(self, ev_connection: EasyvereinAPI, example_custom_field, example_member):
        member_custom_field = ev_connection.member.custom_field(example_member.id).ensure_set(
            example_custom_field.id, "Ensured-Value"
        )
        assert member_custom_field.value == "Ensured-Value"

    def test_ensure_custom_field_value_empty(self, ev_connection: EasyvereinAPI, example_custom_field, example_member):
        member_custom_field = ev_connection.member.custom_field(example_member.id).ensure_set(
            example_custom_field.id, "New-Ensured-Value"
        )

        assert member_custom_field.value == "New-Ensured-Value"

        member_custom_field = ev_connection.member.custom_field(example_member.id).ensure_set(
            example_custom_field.id, ""
        )
        assert member_custom_field.value is None
