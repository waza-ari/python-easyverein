"""
Member related models
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from ..core.types import (
    EasyVereinReference,
    FilterIntList,
    HexColor,
    OptionsField,
    PositiveIntWithZero,
)
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class CustomFieldBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `CustomField` | `CustomFieldUpdate` | `CustomFieldCreate` |

    Custom fields can be used in a variety of places. Currently, the supported types include **member** custom fields,
    **event** custom fields, **contact details** custom fields and **inventory** custom fields.

    !!! info "Custom Field Values"
        This endpoint manages the custom fields themselves, not their values.
    """

    name: str | None = Field(default=None, max_length=200)
    color: HexColor = None
    short: str | None = Field(default=None, max_length=4)
    orderSequence: PositiveIntWithZero | None = None
    settings_type: Literal["t", "f", "z", "d", "c", "r", "s", "a", "b", "m"] | None = None
    """
    Settings type defines which type of field this custom field should be. Possible values:

    - t: Single line text field
    - f: Multiline text field
    - z: Digit text field
    - d: Date field
    - c: Checkbox
    - r: Date range field (from date and to date)
    - s: Select field
    - a: Multiselect field
    - b: File upload
    - m: reminder

    If type is set to s or a, the possible options need to be defined in the additional field
    """
    kind: Literal["a", "b", "ba", "ca", "iv", "t", "u", "ic", "c", "e", "h", "j", "i", "k"] | None = None
    """
    Kind defines in which context this custom field is used. Unfortunately only some possible values are
    documented in the API spec:

    - e: for members
    - h: for events
    - j: for contact details
    - i: for inventory function

    It is not even possible to set other fields except the ones mentioned before in the portal,
    so not sure what the other values are meant for.
    """
    additional: OptionsField = None
    description: str | None = Field(default=None, max_length=124)
    member_show: bool | None = None
    member_edit: bool | None = None
    needsAdminApproval: bool | None = None
    member_dsgvo: bool | None = None
    position: PositiveIntWithZero | None = None
    # TODO: Add reference to CustomFieldCollection once implemented
    collection: EasyVereinReference | None = None


class CustomField(CustomFieldBase, EmptyStringsToNone):
    """
    Pydantic model used to represent a custom field
    """

    pass


class CustomFieldCreate(CustomFieldBase, required_mixin(["name", "settings_type", "kind"])):  # type: ignore
    """
    Pydantic model for creating a new custom field
    """


class CustomFieldUpdate(CustomFieldBase):
    """
    Pydantic model used to update a custom field
    """

    pass


class CustomFieldFilter(BaseModel):
    """
    Pydantic model used to filter custom fields
    """

    id__in: FilterIntList | None = None
    name: str | None = None
    color: str | None = None
    kind: str | None = None
    member_edit: bool | None = None
    member_show: bool | None = None
    deletedBy__isnull: bool = Field(default=None, serialization_alias="_deletedBy__isnull")
    deleted: bool | None = None
    ordering: str | None = None
