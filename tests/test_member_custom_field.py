import pytest

from easyverein import EasyvereinAPI
from easyverein.models import (
    MemberCustomField,
    MemberCustomFieldCreate,
    MemberCustomFieldUpdate,
)


@pytest.fixture(scope="class")
def example_member_custom_field(
    ev_connection: EasyvereinAPI, example_member, example_custom_field
):
    member_custom_field = ev_connection.member_custom_field.create(
        MemberCustomFieldCreate(
            customField=example_custom_field.id, value="Example-Value"
        ),
        member_id=example_member.id,
    )
    yield member_custom_field
    ev_connection.member_custom_field.delete(
        member_custom_field, member_id=example_member.id
    )


class TestMemberCustomField:
    def test_create_custom_field(
        self, ev_connection: EasyvereinAPI, example_member, example_custom_field
    ):
        member_custom_field = ev_connection.member_custom_field.create(
            MemberCustomFieldCreate(
                customField=example_custom_field.id, value="Example-Value"
            ),
            member_id=example_member.id,
        )
        assert isinstance(member_custom_field, MemberCustomField)
        assert member_custom_field.value == "Example-Value"

        # Delete it again
        ev_connection.member_custom_field.delete(member_custom_field)

    def test_modify_custom_field(
        self, ev_connection: EasyvereinAPI, example_member_custom_field, example_member
    ):
        member_custom_field = ev_connection.member_custom_field.update(
            example_member_custom_field.id,
            MemberCustomFieldUpdate(value="Modified-Value"),
            member_id=example_member.id,
        )

        # Check that the value was modified
        assert member_custom_field.value == "Modified-Value"

    def test_ensure_custom_field_value(
        self, ev_connection: EasyvereinAPI, example_custom_field, example_member
    ):
        member_custom_field = ev_connection.member_custom_field.ensure_set(
            example_member.id, example_custom_field.id, "Ensured-Value"
        )
        assert member_custom_field.value == "Ensured-Value"
