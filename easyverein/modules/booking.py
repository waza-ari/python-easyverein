"""
All methods related to bookings
"""

import logging

from ..core.client import EasyvereinClient
from ..models.booking import (
    Booking,
    BookingCreate,
    BookingFilter,
    BookingUpdate,
)
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class BookingMixin(
    CRUDMixin[Booking, BookingCreate, BookingUpdate, BookingFilter],
    RecycleBinMixin[Booking],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "booking"
        self.return_type = Booking
        self.c = client
        self.logger = logger
