"""
Member related models
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, PositiveInt

from ..core.types import (
    Date,
    EasyVereinReference,
    HexColor,
    OptionsField,
    PositiveIntWithZero,
)
from .mixins.required_attributes import required_mixin


class CustomField(BaseModel):
    """
    Pydantic model representing an Invoice
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None
    # TODO: Add reference to Organization once implemented
    _deleteAfterDate: Date | None = None
    _deletedBy: str | None = None
    name: str | None = Field(default=None, max_length=200)
    color: HexColor = None
    short: str | None = Field(default=None, max_length=4)
    orderSequence: PositiveIntWithZero | None = None
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
    settings_type: Literal[
        "t", "f", "z", "d", "c", "r", "s", "a", "b", "m"
    ] | None = None
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
    kind: Literal[
        "a", "b", "ba", "ca", "iv", "t", "u", "ic", "c", "e", "h", "j", "i", "k"
    ] | None = None
    additional: OptionsField = None
    description: str | None = Field(default=None, max_length=124)
    member_show: bool | None = None
    member_edit: bool | None = None
    needsAdminApproval: bool | None = None
    member_dsgvo: bool | None = None
    position: PositiveIntWithZero | None = None
    # TODO: Add reference to CustomFieldCollection once implemented
    collection: EasyVereinReference | None = None


class CustomFieldCreate(CustomField, required_mixin(["name", "settings_type", "kind"])):
    """
    Pydantic model for creating a new member
    """


class CustomFieldUpdate(CustomField):
    """
    Pydantic model used to update a member
    """

    pass
