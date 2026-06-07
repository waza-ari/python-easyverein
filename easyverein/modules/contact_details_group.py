"""
All methods related to custom fields
"""

import logging

from ..core.client import EasyvereinClient
from ..models import (
    ContactDetailsGroup,
    ContactDetailsGroupCreate,
    ContactDetailsGroupFilter,
    ContactDetailsGroupUpdate,
)
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class ContactDetailsGroupMixin(
    CRUDMixin[ContactDetailsGroup, ContactDetailsGroupCreate, ContactDetailsGroupUpdate, ContactDetailsGroupFilter],
    RecycleBinMixin[ContactDetailsGroup],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "contact-details-group"
        self.return_type = ContactDetailsGroup
        self.c = client
        self.logger = logger
