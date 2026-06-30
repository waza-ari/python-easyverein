"""
All methods related to contact details
"""

import logging

from ..core.client import EasyvereinClient
from ..models import BookingProject, BookingProjectCreate, BookingProjectUpdate
from ..models.booking_project import BookingProjectFilter
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class BookingProjectMixin(
    CRUDMixin[BookingProject, BookingProjectCreate, BookingProjectUpdate, BookingProjectFilter],
    RecycleBinMixin[BookingProject],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        self.endpoint_name = "booking-project"
        self.return_type = BookingProject
        self.c = client
        self.logger = logger
