from easyverein import EasyvereinAPI
from easyverein.models import ContactDetails, ContactDetailsCreate, ContactDetailsUpdate


class TestContactDetails:
    def test_get_contact_details(self, ev_connection: EasyvereinAPI):
        contact_details = ev_connection.contact_details.get()
        # Check if the response is a list
        assert isinstance(contact_details, list)

        # We should have 5 invoices based on the example data
        assert len(contact_details) == 6

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

        # Delete the contact details again, should only soft delete them
        ev_connection.contact_details.delete(contact_details)

        # Get entries from wastebasket
        deleted_contact_details = ev_connection.contact_details.get_deleted()
        assert len(deleted_contact_details) == 1

        # Finally purge contact details from wastebasket
        ev_connection.contact_details.purge(contact_details.id)

        # Get entries from wastebasket
        deleted_contact_details = ev_connection.contact_details.get_deleted()
        assert len(deleted_contact_details) == 0

    def test_create_minimal_personal_contact_details(
        self, ev_connection: EasyvereinAPI
    ):
        contact_details = ev_connection.contact_details.create(
            ContactDetailsCreate(isCompany=False, firstName="Test", familyName="Person")
        )

        assert isinstance(contact_details, ContactDetails)
        assert contact_details.isCompany is False
        assert contact_details.firstName == "Test"
        assert contact_details.familyName == "Person"

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
        ev_connection.contact_details.delete(
            contact_details, delete_from_recycle_bin=True
        )
