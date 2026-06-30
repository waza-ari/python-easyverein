from pydantic import BaseModel, PositiveInt

from easyverein.core.types import FilterIntList
from easyverein.models.base import EasyVereinBase
from easyverein.models.mixins.empty_strings_mixin import EmptyStringsToNone

from .mixins.required_attributes import required_mixin


class BookingProjectBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `BookingProject` | `BookingProjectUpdate` | `BookingProjectCreate` |
    """

    name: str
    short: str | None = None
    color: str | None = None
    budget: float | None = None
    completed: bool | None = None
    projectCostCentre: str | None = None


class BookingProject(BookingProjectBase, EmptyStringsToNone):
    """
    Pydantic model for booking project
    """

    pass


class BookingProjectUpdate(BookingProjectBase):
    """
    Pydantic model used to update booking project
    """


class BookingProjectCreate(BookingProjectUpdate, required_mixin(["short"])):  # type: ignore
    """
    Pydantic model for creating new booking project
    """


class BookingProjectFilter(BaseModel):
    """
    Pydantic model used to filter booking project
    """

    id__in: FilterIntList | None = None
    budget__lt: PositiveInt | None = None
    budget__gt: PositiveInt | None = None
    completed: bool | None = None
    name: str | None = None
    short: str | None = None
    ordering: str | None = None
    search: str | None = None
