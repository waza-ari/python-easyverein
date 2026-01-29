"""
All methods related to invoices
"""

import logging

from easyverein.modules.member_custom_field import MemberCustomFieldMixin
from easyverein.modules.member_member_group import MemberMemberGroupMixin

from ..core.client import EasyvereinClient
from ..models import Member, MemberCreate, MemberFilter, MemberSetLsb, MemberUpdate
from ..models.member import MemberSetDosb
from .mixins.crud import BulkUpdateCreateMixin, CRUDMixin
from .mixins.helper import get_id
from .mixins.recycle_bin import RecycleBinMixin


class MemberMixin(
    CRUDMixin[Member, MemberCreate, MemberUpdate, MemberFilter],
    BulkUpdateCreateMixin[Member, MemberCreate, MemberUpdate],
    RecycleBinMixin[Member],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "member"
        self.c = client
        self.logger = logger
        self.return_type = Member

    def custom_field(self, member_id: int) -> MemberCustomFieldMixin:
        return MemberCustomFieldMixin(self.c, self.logger, member_id)

    def member_group(self, member_id: int) -> MemberMemberGroupMixin:
        return MemberMemberGroupMixin(self.c, self.logger, member_id)

    def set_lsb(self, target: Member | int, data: MemberSetLsb) -> None:
        obj_id = get_id(target)

        self.logger.info(f"Setting LSB sports for member {obj_id}")

        url = self.c.get_url(f"/{self.endpoint_name}/{obj_id}/set-lsb")
        self.c.update(url, data, status_code=204)

    def set_dosb(self, target: Member | int, data: MemberSetDosb) -> None:
        obj_id = get_id(target)

        self.logger.info(f"Setting DOSB sports for member {obj_id}")

        url = self.c.get_url(f"/{self.endpoint_name}/{obj_id}/set-dosb")
        self.c.update(url, data, status_code=204)
