from typing import Generator

import pytest
from easyverein import EasyvereinAPI
from easyverein.models import ContactDetails, ContactDetailsCreate, ContactDetailsUpdate


@pytest.fixture(scope="module", autouse=True)
def _remove_test_contacts(ev_connection: EasyvereinAPI) -> Generator[None, None, None]:
    yield
    for c in ev_connection.contact_details.get_all(query="{id,firstName}"):
        if c.firstName and c.firstName.lower().startswith("test_"):
            ev_connection.contact_details.delete(c, delete_from_recycle_bin=True)


class TestContactDetails:
    def test_get_contact_details(self, ev_connection: EasyvereinAPI):
        contact_details, total_count = ev_connection.contact_details.get()
        # Check if the response is a list
        assert isinstance(contact_details, list)

        # We should have contacts based on the example data
        assert total_count == 8
        assert len(contact_details) == 8

        # Check if all the members are of type Member
        for contact_detail in contact_details:
            assert isinstance(contact_detail, ContactDetails)

    def test_create_minimal_company_contact_details(self, ev_connection: EasyvereinAPI):
        contact_details = ev_connection.contact_details.create(
            ContactDetailsCreate(isCompany=True, companyName="Test Company")
        )
        assert isinstance(contact_details, ContactDetails)
        assert contact_details.isCompany is True
        assert contact_details.companyName == "Test Company"
        assert isinstance(contact_details.id, int)

        # Delete the contact details again, should only soft delete them
        ev_connection.contact_details.delete(contact_details)

        # Get entries from wastebasket
        deleted_contact_details, _ = ev_connection.contact_details.get_deleted()
        assert len(deleted_contact_details) == 1

        # Finally purge contact details from wastebasket
        ev_connection.contact_details.purge(contact_details.id)

        # Get entries from wastebasket
        deleted_contact_details, _ = ev_connection.contact_details.get_deleted()
        assert len(deleted_contact_details) == 0

    def test_create_minimal_personal_contact_details(self, ev_connection: EasyvereinAPI):
        contact_details = ev_connection.contact_details.create(
            ContactDetailsCreate(isCompany=False, firstName="Test", familyName="Person")
        )

        assert isinstance(contact_details, ContactDetails)
        assert contact_details.isCompany is False
        assert contact_details.firstName == "Test"
        assert contact_details.familyName == "Person"
        assert isinstance(contact_details.id, int)

        # Modify the contact details to include address
        contact_details = ev_connection.contact_details.update(
            contact_details.id,
            ContactDetailsUpdate(
                street="Test-Street 1",
                zip="12345",
                city="Test-City",
                country="Deutschland",
            ),
        )

        assert isinstance(contact_details, ContactDetails)
        assert contact_details.street == "Test-Street 1"
        assert contact_details.zip == "12345"
        assert contact_details.city == "Test-City"
        assert contact_details.country == "Deutschland"

        # Delete the contact details again
        ev_connection.contact_details.delete(contact_details, delete_from_recycle_bin=True)


class TestContactDetailsBulk:
    def test_bulk_create(self, ev_connection: EasyvereinAPI, random_string: str):
        name = random_string
        contact_details_data = [
            ContactDetailsCreate(firstName=f"test_{name}1", familyName="Person", isCompany=False),
            ContactDetailsCreate(firstName=f"test_{name}2", familyName="Person", isCompany=False),
        ]

        successes = ev_connection.contact_details.bulk_create(contact_details_data)
        assert successes == [True, True]

        created_contacts = [
            c
            for c in ev_connection.contact_details.get_all(query="{id,firstName}")
            if c.firstName and c.firstName.startswith(f"test_{name}")
        ]

        assert isinstance(created_contacts, list)
        assert len(created_contacts) == 2

    def test_bulk_update(self, ev_connection: EasyvereinAPI, random_string: str):
        # We need some contacts to update. Let's create two.
        name = random_string
        c1 = ev_connection.contact_details.create(
            ContactDetailsCreate(firstName=f"test_{name}3", familyName="Person", isCompany=False)
        )
        c2 = ev_connection.contact_details.create(
            ContactDetailsCreate(firstName=f"test_{name}4", familyName="Person", isCompany=False)
        )

        update_data = [
            ContactDetailsUpdate(id=c1.id, street="Test Street 1"),
            ContactDetailsUpdate(id=c2.id, street="Test Street 2"),
        ]

        successes = ev_connection.contact_details.bulk_update(update_data)
        assert successes == [True, True]

        updated_c1 = ev_connection.contact_details.get_by_id(c1.id)  # type: ignore
        updated_c2 = ev_connection.contact_details.get_by_id(c2.id)  # type: ignore

        assert updated_c1.street == "Test Street 1"
        assert updated_c2.street == "Test Street 2"
