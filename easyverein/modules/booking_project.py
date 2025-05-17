"""
BookingProject API module
"""

from ..models.booking_project import (
    BookingProject,
    BookingProjectCreate,
    BookingProjectFilter,
    BookingProjectUpdate,
)
from .mixins.crud import CRUDMixin


class BookingProjectModule(CRUDMixin):
    """
    Module for interacting with BookingProject API endpoints
    """

    _plural_name = "booking-projects"
    _model = BookingProject
    _creation_model = BookingProjectCreate
    _update_model = BookingProjectUpdate
    _filter_model = BookingProjectFilter
