from easyverein.core.types import FilterIntList, HexColor
from easyverein.models.base import EasyVereinBase, EasyVereinFilter
from easyverein.models.mixins.empty_strings_mixin import EmptyStringsToNone

from .mixins.required_attributes import required_mixin


class BookingProjectBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `BookingProject` | `BookingProjectUpdate` | `BookingProjectCreate` |
    """

    name: str | None = None
    short: str | None = None
    color: HexColor = None
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


class BookingProjectCreate(BookingProjectUpdate, required_mixin(["name", "short"])):  # type: ignore
    """
    Pydantic model for creating new booking project
    """


class BookingProjectFilter(EasyVereinFilter):
    """
    Pydantic model used to filter booking project
    """

    id__in: FilterIntList | None = None
    budget__lt: float | None = None
    budget__gt: float | None = None
    completed: bool | None = None
    name: str | None = None
    short: str | None = None
    ordering: str | None = None
    search: str | None = None
