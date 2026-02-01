"""
All methods related to invoices
"""

import logging

from ..core.client import EasyvereinClient
from ..models import (
    CustomField,
    CustomFieldSelectOption,
    Member,
    MemberCustomField,
    MemberCustomFieldCreate,
    MemberCustomFieldFilter,
    MemberCustomFieldUpdate,
)
from .mixins.crud import CRUDMixin
from .mixins.helper import get_id


class MemberCustomFieldMixin(
    CRUDMixin[MemberCustomField, MemberCustomFieldCreate, MemberCustomFieldUpdate, MemberCustomFieldFilter]
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger, member: Member | int):
        self.return_type = MemberCustomField
        self.c = client
        self.logger = logger
        self.member_id = get_id(member)

    @property
    def endpoint_name(self) -> str:
        return f"member/{self.member_id}/custom-fields"

    def ensure_set(self, custom_field_id: int, value: str | list[str]) -> MemberCustomField:
        """
        Convenience method to set the custom field value on a member, no matter if it was
        set before already (PATCH) or not.

        For select (s) and multiselect (a) custom fields, you can provide a list of values.
        Instead of using the value, the method will automatically fetch and select the
        options from selectOptions that have been introduced in January 2026.

        Regarding rate limiting, be aware that this method requires at least two API calls.

        Args:
            custom_field_id (int): Custom field ID that should be set or changed
            value (str | list[str]): New value the specified custom field should be set to
        """
        custom_field_query = "{id,settings_type,selectOptions{id,value}}"
        custom_field = self.c.api_instance.custom_field.get_by_id(custom_field_id, query=custom_field_query)
        use_selected_options = custom_field.settings_type in ("s", "a")

        if use_selected_options:
            values_list = [value] if isinstance(value, str) else list(value)
            value_to_id: dict[str, int] = {}
            for opt in custom_field.selectOptions or []:
                if isinstance(opt, CustomFieldSelectOption) and opt.id is not None and opt.value:
                    value_to_id[opt.value] = opt.id
            option_ids = [value_to_id[v] for v in values_list if v in value_to_id]
            missing = [v for v in values_list if v not in value_to_id]
            if missing:
                raise ValueError(f"No select option(s) with value(s) {missing!r} for custom field {custom_field_id}")
            payload_value = None
            payload_selected_options: list[int] | None = option_ids
        else:
            assert isinstance(value, str), "Value must be a string for non-select custom fields"
            payload_value = value
            payload_selected_options = None

        # Get all custom fields this member has already set, use max limit available
        query = "{id,value,customField{id}}"
        all_member_custom_fields = self.get_all(limit_per_page=100, query=query)

        # Extract custom field from that list if it exists
        existing_custom_field = next(
            (
                mcf
                for mcf in all_member_custom_fields
                if isinstance(mcf.customField, CustomField) and mcf.customField.id == custom_field_id
            ),
            None,
        )

        if existing_custom_field:
            # It's already there, we need to patch the existing field
            patch = MemberCustomFieldUpdate(value=payload_value, selectedOptions=payload_selected_options)
            assert existing_custom_field.id
            return self.update(existing_custom_field.id, patch)
        else:
            # It's not there, we need to create it
            create = MemberCustomFieldCreate(
                customField=custom_field_id, value=payload_value, selectedOptions=payload_selected_options
            )
            return self.create(create)
