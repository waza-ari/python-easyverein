import logging
from typing import Any

from ..core.api_version import API_V3
from ..core.client import EasyvereinClient
from ..models import (
    CustomField,
    CustomFieldSelectOption,
    CustomFieldSelectOptionCreate,
    CustomFieldSelectOptionFilter,
    CustomFieldSelectOptionUpdate,
)
from .mixins.crud import CRUDMixin
from .mixins.helper import get_id


class CustomFieldSelectOptionMixin(
    CRUDMixin[
        CustomFieldSelectOption,
        CustomFieldSelectOptionCreate,
        CustomFieldSelectOptionUpdate,
        CustomFieldSelectOptionFilter,
    ]
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger, custom_field: CustomField | int):
        self.return_type = CustomFieldSelectOption
        self.c = client
        self.logger = logger
        self.custom_field_id = get_id(custom_field)

    @property
    def endpoint_name(self) -> str:
        if self.c.api_version == API_V3:
            return "select-option"
        return f"custom-field/{self.custom_field_id}/select-options"

    @property
    def scope_params(self) -> dict[str, Any]:
        return {"custom_field": self.custom_field_id} if self.c.api_version == API_V3 else {}

    def create(self, data: CustomFieldSelectOptionCreate) -> CustomFieldSelectOption:
        """
        Creates a select option for this custom field and returns the created object.

        Args:
            data: Object to be created. `customField` is set to this custom field if not given
                (required by API v3.0).
        """
        if self.c.api_version == API_V3 and data.customField is None:
            data = data.model_copy(update={"customField": self.custom_field_id})
        return super().create(data)
