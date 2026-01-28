"""
All methods related to invoices
"""

import logging

from ..core.client import EasyvereinClient
from ..core.exceptions import EasyvereinAPIException
from ..models import (
    Member,
    MemberGroup,
    MemberMemberGroup,
    MemberMemberGroupCreate,
    MemberMemberGroupFilter,
    MemberMemberGroupUpdate,
)
from .mixins.crud import CRUDMixin
from .mixins.helper import get_id


class MemberMemberGroupMixin(
    CRUDMixin[
        MemberMemberGroup,
        MemberMemberGroupCreate,
        MemberMemberGroupUpdate,
        MemberMemberGroupFilter,
    ]
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger, member: Member | int):
        self.return_type = MemberMemberGroup
        self.c = client
        self.logger = logger
        self.member_id = get_id(member)

    @property
    def endpoint_name(self) -> str:
        return f"member/{self.member_id}/groups"

    def get_group_membership(self, group: MemberGroup | int) -> MemberMemberGroup | None:
        """
        Returns the membership object of this member in the given group, None if the member is not in the group.

        This method can be useful if the group membership should be updated or deleted.

        Args:
            group: The group object or id to fetch.
        """
        group_id = get_id(group)
        self.logger.info(f"Fetching members of group {group_id}")

        search = MemberMemberGroupFilter(memberGroup=group_id)
        result, _ = self.get(search=search)
        return result[0] if result else None

    def add_to_group(self, group: MemberGroup | int, payment_active: bool = False, ignore_existing: bool = False):
        """
        Adds a member to a group. Will silently ignore if the member is already in the group,
        unless ignore_existing is set to False.

        Args:
            group: The group object or id to add the member to.
            payment_active: If set to True, the group will be activated for billing purposes
            ignore_existing: If set to False, will raise an exception if the member is already in the group.
        """
        group_id = get_id(group)
        self.logger.info(f"Adding member {self.member_id} to group {group_id}")

        # if ignore_existing is set, we'll want to check if the member is already in the group
        if self.get_group_membership(group_id) and ignore_existing:
            self.logger.info(f"Member {self.member_id} is already in group {group_id}, ignoring")
            return None

        return self.create(
            MemberMemberGroupCreate(userObject=self.member_id, memberGroup=group_id, paymentActive=payment_active)
        )

    def remove_from_group(self, group: MemberGroup | int):
        """
        Removes a member from a group. Raises an exception if the member is not in the group.

        Args:
            group: The group object or id to remove the member from.
        """
        group_id = get_id(group)
        self.logger.info(f"Removing member {self.member_id} from group {group_id}")

        membership = self.get_group_membership(group_id)
        if not membership or not membership.id:
            raise EasyvereinAPIException(f"Member {self.member_id} is not in group {group_id}")

        return self.delete(membership.id)

    def set_group_billing_status(self, group: MemberGroup | int, new_billing_status: bool):
        """
        Activates or deactivates the membership of the member in the given group for billing purposes.
        Returns the updated membership object if successful.
        Raises an exception if the member is not in the group.

        Args:
            group: The group object or id to activate.
            new_billing_status: The new billing status for the group.
        """
        group_id = get_id(group)
        self.logger.info(f"Activating group {group_id} for member {self.member_id}")

        membership = self.get_group_membership(group_id)
        if not membership or not membership.id:
            raise EasyvereinAPIException(f"Member {self.member_id} is not in group {group_id}")

        return self.update(membership.id, MemberMemberGroupUpdate(paymentActive=new_billing_status))
