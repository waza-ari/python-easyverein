from __future__ import annotations

from pydantic import BaseModel, PositiveInt

from ..core.types import EasyVereinReference, FilterIntList, FilterStrList, PositiveIntWithZero, Sphere
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class BillingAccountBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `BillingAccount` | `BillingAccountUpdate` | `BillingAccountCreate` |
    """

    name: str | None = None
    excludeInEur: bool | None = None
    number: PositiveInt | None = None
    defaultSphere: Sphere | None = None


class BillingAccount(BillingAccountBase, EmptyStringsToNone):
    """
    Pydantic model representing an BillingAccount
    """

    skr: str | None = None
    accountingPlans: list[EasyVereinReference] | None = None
    numberLength: PositiveIntWithZero
    linkedBookings: PositiveIntWithZero


class BillingAccountCreate(
    BillingAccountBase,
    required_mixin(["name", "number"]),  # type: ignore
):
    """
    Pydantic model representing a BillingAccount
    """


class BillingAccountUpdate(BillingAccountBase):
    """
    Pydantic model used to patch an BillingAccount
    """


class BillingAccountFilter(BaseModel):
    """
    Pydantic model used to filter billing accounts
    """

    id__in: FilterIntList | None = None
    name: str | None = None
    skr: str | None = None
    skr__in: FilterStrList | None = None
    number__gte: PositiveInt | None = None
    number__lte: PositiveInt | None = None
    deleted: bool | None = None
    accountingPlan__isnull: bool | None = None
    showOwnBillingAccounts: bool | None = None
    ordering: str | None = None
    search: str | None = None
