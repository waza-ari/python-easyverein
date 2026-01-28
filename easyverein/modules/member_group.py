"""
All methods related to custom fields
"""

import logging

from ..core.client import EasyvereinClient
from ..models import MemberGroup, MemberGroupCreate, MemberGroupFilter, MemberGroupUpdate
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class MemberGroupMixin(
    CRUDMixin[MemberGroup, MemberGroupCreate, MemberGroupUpdate, MemberGroupFilter],
    RecycleBinMixin[MemberGroup],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "member-group"
        self.return_type = MemberGroup
        self.c = client
        self.logger = logger
