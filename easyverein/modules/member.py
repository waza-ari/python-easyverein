"""
All methods related to invoices
"""

import logging

from easyverein.modules.member_custom_field import MemberCustomFieldMixin
from easyverein.modules.member_member_group import MemberMemberGroupMixin

from ..core.client import EasyvereinClient
from ..models import Member, MemberCreate, MemberFilter, MemberUpdate
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class MemberMixin(CRUDMixin[Member, MemberCreate, MemberUpdate, MemberFilter], RecycleBinMixin[Member]):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "member"
        self.c = client
        self.logger = logger
        self.return_type = Member

    def custom_field(self, member_id: int) -> MemberCustomFieldMixin:
        return MemberCustomFieldMixin(self.c, self.logger, member_id)

    def member_group(self, member_id: int) -> MemberMemberGroupMixin:
        return MemberMemberGroupMixin(self.c, self.logger, member_id)
