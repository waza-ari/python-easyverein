"""
All methods related to billing accounts
"""

import logging

from ..core.client import EasyvereinClient
from ..models.billing_account import (
    BillingAccount,
    BillingAccountCreate,
    BillingAccountFilter,
    BillingAccountUpdate,
)
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class BillingAccountMixin(
    CRUDMixin[BillingAccount, BillingAccountCreate, BillingAccountUpdate, BillingAccountFilter],
    RecycleBinMixin[BillingAccount],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "billing-account"
        self.return_type = BillingAccount
        self.c = client
        self.logger = logger
