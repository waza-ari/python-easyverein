import time
from typing import Generator

import pytest
from easyverein import EasyvereinAPI
from easyverein.models import (
    ContactDetailsGroup,
    ContactDetailsGroupCreate,
    ContactDetailsGroupFilter,
    ContactDetailsGroupUpdate,
)


@pytest.fixture(scope="module", autouse=True)
def _remove_test_contact_details_groups(ev_connection: EasyvereinAPI) -> Generator[None, None, None]:
    yield

    groups = ev_connection.contact_details_group.get_all(query="{id,name}")
    for group in groups:
        if group.name and group.name.startswith("test_contact_details_group_"):
            ev_connection.contact_details_group.delete(group)

    deleted_groups, _ = ev_connection.contact_details_group.get_deleted()
    for group in deleted_groups:
        if group.name and group.name.startswith("test_contact_details_group_"):
            ev_connection.contact_details_group.purge(group)


class TestContactDetailsGroup:
    def test_create_update_filter_and_recycle_bin(self, ev_connection: EasyvereinAPI, random_string: str):
        name = f"test_contact_details_group_{random_string}"
        short = random_string[-4:]

        contact_details_group = ev_connection.contact_details_group.create(
            ContactDetailsGroupCreate(name=name, color="#FF0000", short=short)
        )
        assert isinstance(contact_details_group, ContactDetailsGroup)
        assert isinstance(contact_details_group.id, int)
        assert contact_details_group.name == name
        assert contact_details_group.color == "#FF0000"
        assert contact_details_group.short == short

        filtered_groups, total_count = ev_connection.contact_details_group.get(
            search=ContactDetailsGroupFilter(name=name)
        )
        assert total_count >= 1
        assert any(group.id == contact_details_group.id for group in filtered_groups)

        updated_group = ev_connection.contact_details_group.update(
            contact_details_group.id,
            ContactDetailsGroupUpdate(color="#00FF00", short="TCDG"),
        )
        assert isinstance(updated_group, ContactDetailsGroup)
        assert updated_group.id == contact_details_group.id
        assert updated_group.color == "#00FF00"
        assert updated_group.short == "TCDG"

        fetched_group = ev_connection.contact_details_group.get_by_id(contact_details_group.id)
        assert fetched_group.id == contact_details_group.id
        assert fetched_group.color == "#00FF00"
        assert fetched_group.short == "TCDG"

        ev_connection.contact_details_group.delete(contact_details_group)

        time.sleep(1)

        deleted_groups, _ = ev_connection.contact_details_group.get_deleted()
        deleted_group = next((group for group in deleted_groups if group.id == contact_details_group.id), None)
        assert deleted_group is not None
        assert deleted_group.name == name

        ev_connection.contact_details_group.purge(contact_details_group.id)

        deleted_groups, _ = ev_connection.contact_details_group.get_deleted()
        assert all(group.id != contact_details_group.id for group in deleted_groups)
