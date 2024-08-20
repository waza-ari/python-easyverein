"""
All methods related to invoices
"""

import logging

from ..core.client import EasyvereinClient
from ..models import (
    CustomField,
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

    def ensure_set(self, custom_field_id: int, value: str) -> MemberCustomField:
        """
        Convenience method to set the custom field value on a member, no matter if it was
        set before already (PATCH) or not.

        Regarding rate limiting, be aware that this method requires at least two API calls.

        Args:
            custom_field_id (int): Custom field ID that should be set or changed
            value (str): New value the specified custom field should be set to
        """

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
            patch = MemberCustomFieldUpdate(value=value)
            assert existing_custom_field.id
            return self.update(existing_custom_field.id, patch)
        else:
            # It's not there, we need to create it
            create = MemberCustomFieldCreate(value=value, customField=custom_field_id)
            return self.create(create)
