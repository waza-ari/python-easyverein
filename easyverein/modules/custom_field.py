"""
All methods related to custom fields
"""

import logging

from ..core.client import EasyvereinClient
from ..models.custom_field import (
    CustomField,
    CustomFieldCreate,
    CustomFieldFilter,
    CustomFieldUpdate,
)
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class CustomFieldMixin(
    CRUDMixin[CustomField, CustomFieldCreate, CustomFieldUpdate, CustomFieldFilter],
    RecycleBinMixin[CustomField],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "custom-field"
        self.return_type = CustomField
        self.c = client
        self.logger = logger
