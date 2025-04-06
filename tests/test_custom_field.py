from easyverein import EasyvereinAPI
from easyverein.models.custom_field import (
    CustomField,
    CustomFieldCreate,
    CustomFieldUpdate,
)


class TestCustomField:
    def test_create_custom_field(self, ev_connection: EasyvereinAPI):
        # Get current custom fields
        _, old_total_count = ev_connection.custom_field.get()

        custom_field = ev_connection.custom_field.create(
            CustomFieldCreate(name="Test-Field", kind="e", settings_type="t")
        )
        assert isinstance(custom_field, CustomField)
        assert custom_field.name == "Test-Field"

        # Get all custom fields and check that we've got one more than the 40 built-in now
        custom_fields, total_count = ev_connection.custom_field.get()
        assert isinstance(custom_fields, list)
        assert total_count == old_total_count + 1
        assert all(isinstance(f, CustomField) for f in custom_fields)
        assert isinstance(custom_field.id, int)

        # Change the name of the custom field
        cf = ev_connection.custom_field.update(custom_field.id, CustomFieldUpdate(name="Changed-Name"))

        assert isinstance(cf, CustomField)
        assert cf.name == "Changed-Name"

        # Change type to date
        cf = ev_connection.custom_field.update(custom_field.id, CustomFieldUpdate(settings_type="d"))

        assert isinstance(cf, CustomField)
        assert cf.settings_type == "d"

        # Change kind to contact details
        cf = ev_connection.custom_field.update(custom_field.id, CustomFieldUpdate(kind="j"))

        assert isinstance(cf, CustomField)
        assert cf.kind == "j"

        # Delete custom field again
        ev_connection.custom_field.delete(custom_field)

        # Now there should be the original count left
        custom_fields, total_count = ev_connection.custom_field.get()
        assert isinstance(custom_fields, list)
        assert total_count == old_total_count

        # There should be one deleted custom field in the recycle bin
        deleted_custom_fields, _ = ev_connection.custom_field.get_deleted()
        assert isinstance(deleted_custom_fields, list)
        assert len(deleted_custom_fields) == 1
        assert isinstance(deleted_custom_fields[0], CustomField)
        assert deleted_custom_fields[0].id == custom_field.id
        assert deleted_custom_fields[0].name == "Changed-Name"

        # Finally purge custom field from wastebasket
        ev_connection.custom_field.purge(custom_field.id)

        # Get entries from wastebasket
        deleted_custom_fields, _ = ev_connection.custom_field.get_deleted()
        assert isinstance(deleted_custom_fields, list)
        assert len(deleted_custom_fields) == 0
        assert len(custom_fields) == old_total_count
