"""
All methods related to invoices
"""

import logging

from ..core.client import EasyvereinClient
from ..models.member import Member, MemberCreate, MemberFilter, MemberUpdate
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class MemberMixin(
    CRUDMixin[Member, MemberCreate, MemberUpdate, MemberFilter], RecycleBinMixin[Member]
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "member"
        self.return_type = Member
        self.c = client
        self.logger = logger
