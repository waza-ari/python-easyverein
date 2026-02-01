from typing import Literal, cast

from easyverein import EasyvereinAPI
from easyverein.models.custom_field import CustomField, CustomFieldCreate
from easyverein.models.custom_field_select_option import (
    CustomFieldSelectOption,
    CustomFieldSelectOptionCreate,
    CustomFieldSelectOptionUpdate,
)


class TestCustomFieldSelectOption:
    def test_select_and_multiselect_custom_field_with_select_options(self, ev_connection: EasyvereinAPI):
        for settings_type, field_name in [("s", "Test-Select-Field"), ("a", "Test-Multiselect-Field")]:
            custom_field = ev_connection.custom_field.create(
                CustomFieldCreate(
                    name=field_name,
                    kind="e",
                    settings_type=cast(Literal["s", "a"], settings_type),
                )
            )
            assert isinstance(custom_field, CustomField)
            assert custom_field.settings_type == settings_type
            assert isinstance(custom_field.id, int)

            select_options = ev_connection.custom_field.select_option(custom_field.id)

            # Create select option
            option = select_options.create(CustomFieldSelectOptionCreate(value="Option A"))
            assert isinstance(option, CustomFieldSelectOption)
            assert option.value == "Option A"
            assert isinstance(option.id, int)

            # Create another option
            option_b = select_options.create(CustomFieldSelectOptionCreate(value="Option B", orderSequence=1))
            assert isinstance(option_b, CustomFieldSelectOption)
            assert option_b.value == "Option B"

            # Update first option
            updated_option = select_options.update(
                option.id,
                CustomFieldSelectOptionUpdate(value="Option A Updated"),
            )
            assert isinstance(updated_option, CustomFieldSelectOption)
            assert updated_option.value == "Option A Updated"

            # List options
            options_list, total = select_options.get()
            assert len(options_list) >= 2
            assert all(isinstance(o, CustomFieldSelectOption) for o in options_list)

            # Delete first option
            select_options.delete(option.id)

            options_after_delete, total_after = select_options.get()
            assert total_after == total - 1
            assert not any(o.id == option.id for o in options_after_delete)

            # Delete second option
            select_options.delete(option_b)

            # Delete custom field and purge
            ev_connection.custom_field.delete(custom_field, delete_from_recycle_bin=True)

    def test_multiselect_ensure_set_workflow(self, ev_connection: EasyvereinAPI, example_member):
        """Create type-a field with A/B/C, ensure_set A+B -> A+C -> [] then delete field."""
        custom_field = ev_connection.custom_field.create(
            CustomFieldCreate(
                name="Test-Multiselect-EnsureSet",
                kind="e",
                settings_type="a",
            )
        )
        try:
            assert custom_field.id is not None

            select_options = ev_connection.custom_field.select_option(custom_field.id)
            opt_a = select_options.create(CustomFieldSelectOptionCreate(value="A"))
            opt_b = select_options.create(CustomFieldSelectOptionCreate(value="B"))
            opt_c = select_options.create(CustomFieldSelectOptionCreate(value="C"))
            assert opt_a.id and opt_b.id and opt_c.id

            member_cf = ev_connection.member.custom_field(example_member.id)
            query = "{id,customField{id},selectedOptions{id,value}}"

            def get_selected_values() -> set[str]:
                all_mcf = member_cf.get_all(limit_per_page=100, query=query)
                mcf_for_field = next(
                    (m for m in all_mcf if m.customField and getattr(m.customField, "id", None) == custom_field.id),
                    None,
                )
                if mcf_for_field is None:
                    return set()
                return {
                    opt.value
                    for opt in (mcf_for_field.selectedOptions or [])
                    if isinstance(opt, CustomFieldSelectOption) and opt.value
                }

            mcf = member_cf.ensure_set(custom_field.id, ["A", "B"])
            assert mcf is not None
            assert get_selected_values() == {"A", "B"}

            mcf = member_cf.ensure_set(custom_field.id, ["A", "C"])
            assert mcf is not None
            assert get_selected_values() == {"A", "C"}

            mcf = member_cf.ensure_set(custom_field.id, [])
            assert mcf is not None
            assert get_selected_values() == set()
        finally:
            ev_connection.custom_field.delete(custom_field, delete_from_recycle_bin=True)
