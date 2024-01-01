"""
All methods related to invoices
"""
import logging

from ..core.client import EasyvereinClient
from ..models.member import Member
from .mixins.recycle_bin import recycle_bin_mixin

recycle_mixin = recycle_bin_mixin(Member)


class MemberMixin(recycle_mixin):
    """
    All methods related to invoices
    """

    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "member"
        self.c = client
        self.logger = logger

    def get(self, query: str = None, limit: int = 100) -> list[Member]:
        """
        Fetches all members from the API

        Args:
            query (str, optional): Query to use with API. Defaults to None.
            limit (int, optional): How many resources per request. Defaults to 100.
        """
        self.logger.info("Fetching all members from API")

        url = self.c.get_url(
            f"/{self.endpoint_name}/" + (("?query=" + query) if query else "")
        )

        return self.c.fetch_paginated(url, Member, limit)

    def get_by_id(self, member_id: int) -> Member:
        """
        Fetches a member from the API

        Args:
            member_id (int): ID of the member to fetch
        """
        self.logger.info("Fetching invoice %s from API", member_id)

        url = self.c.get_url(f"/{self.endpoint_name}/{member_id}")

        return self.c.fetch_one(url, Member)

    def delete(
        self,
        member: Member,
        delete_from_recycle_bin: bool = False,
    ):
        """
        Deletes a member

        Args:
            member (Member): Member to delete
            delete_from_recycle_bin (bool, optional): Whether to delete the invoice
                also from the recycle bin. Defaults to False.
        """
        self.logger.info("Deleting member %s", member.id)

        url = self.c.get_url(f"/{self.endpoint_name}/{member.id}")

        self.c.delete(url)

        if delete_from_recycle_bin:
            self.logger.info("Deleting member %s from wastebasket", member.id)
            self.purge(member.id)
