"""
BookingProject API module
"""

import logging

from ..core.client import EasyvereinClient
from ..models.booking_project import (
    BookingProject,
    BookingProjectCreate,
    BookingProjectFilter,
    BookingProjectUpdate,
)
from .mixins.crud import CRUDMixin


class BookingProjectMixin(CRUDMixin):
    """
    Module for interacting with BookingProject API endpoints
    """

    _plural_name = "booking-projects"
    _model = BookingProject
    _creation_model = BookingProjectCreate
    _update_model = BookingProjectUpdate
    _filter_model = BookingProjectFilter

    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "booking-project"
        self.return_type = BookingProject
        self.c = client
        self.logger = logger
