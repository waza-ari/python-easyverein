"""
All methods related to invoices
"""

import logging

from ..core.client import EasyvereinClient
from ..core.protocol import IsEVClientProtocol
from ..models import MemberCustomField, MemberCustomFieldCreate, MemberCustomFieldUpdate
from ..models.member_custom_field import MemberCustomFieldFilter
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class MemberCustomFieldMixin(
    CRUDMixin[
        MemberCustomField,
        MemberCustomFieldCreate,
        MemberCustomFieldUpdate,
        MemberCustomFieldFilter,
    ],
    RecycleBinMixin[MemberCustomField],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.return_type = MemberCustomField
        self.c = client
        self.logger = logger
        self.member_id = None

    @property
    def endpoint_name(self) -> str:
        return f"member/{self.member_id}/custom-fields"

    def get(
        self: IsEVClientProtocol,
        member_id: int = None,
        query: str = None,
        limit: int = 10,
    ) -> list[MemberCustomField]:
        if member_id:
            self.member_id = member_id
        return super().get(query=query, limit=limit)

    def get_all(
        self: IsEVClientProtocol,
        member_id: int = None,
        query: str = None,
        limit_per_page: int = 10,
    ) -> list[MemberCustomField]:
        if member_id:
            self.member_id = member_id
        return super().get_all(query=query, limit_per_page=limit_per_page)

    def get_by_id(
        self: IsEVClientProtocol, obj_id: int, member_id: int = None, query: str = None
    ) -> MemberCustomField:
        if member_id:
            self.member_id = member_id
        return super().get_by_id(obj_id, query=query)

    def create(
        self: IsEVClientProtocol, obj: MemberCustomFieldCreate, member_id: int = None
    ) -> MemberCustomField:
        if member_id:
            self.member_id = member_id
        return super().create(obj)

    def update(
        self: IsEVClientProtocol,
        obj_id: int,
        obj: MemberCustomFieldUpdate,
        member_id: int = None,
    ) -> MemberCustomField:
        if member_id:
            self.member_id = member_id
        return super().update(obj_id, obj)

    def delete(
        self: IsEVClientProtocol,
        obj: MemberCustomField,
        delete_from_recycle_bin: bool = False,
        member_id: int = None,
    ):
        if member_id:
            self.member_id = member_id
        return super().delete(obj, delete_from_recycle_bin)

    def ensure_set(
        self, member_id: int, custom_field_id: int, value: str
    ) -> MemberCustomField:
        """
        Convenience method to set the custom field value on a member, no matter if it was
        set before already (PATCH) or not.

        Regarding rate limiting, be aware that this method requires at least two API calls.

        Args:
            member_id (int): Member ID whose custom field should be set
            custom_field_id (int): Custom field ID that should be set or changed
            value (str): New value the specified custom field should be set to
        """

        self.member_id = member_id

        # Get all custom fields this member has already set, use max limit available
        query = "{id,value,customField{id}}"
        all_member_custom_fields = self.get_all(limit_per_page=100, query=query)

        # Extract custom field from that list if it exists
        existing_custom_field = next(
            (
                mcf
                for mcf in all_member_custom_fields
                if mcf.customField.id == custom_field_id
            ),
            None,
        )

        if existing_custom_field:
            # It's already there, we need to patch the existing field
            patch = MemberCustomFieldUpdate(value=value)
            return self.update(existing_custom_field.id, patch)
        else:
            # It's not there, we need to create it
            create = MemberCustomFieldCreate(value=value, customField=custom_field_id)
            return self.create(create)
