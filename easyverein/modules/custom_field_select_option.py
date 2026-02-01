import logging

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
        return f"custom-field/{self.custom_field_id}/select-options"
