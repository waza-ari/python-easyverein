from __future__ import annotations

from ..core.types import EasyVereinReference
from .base import EasyVereinBase
from .mixins.required_attributes import required_mixin


class MemberCustomField(EasyVereinBase):
    """
    This model represents a custom field associated to a member with a certain value.

    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `MemberCustomField` | `MemberCustomFieldUpdate` | `MemberCustomFieldCreate` |

    As the exact spec differs depending on the usage context of custom fields, this model
    only applies to custom fields used with members.

    Note that the way to change a value of custom field X on member Y depends on the current state:

    - If the MemberCustomField association already exists (that is, if the user had a value
        assigned to this custom field before), you have to PATCH / update the existing object
        In this case you need to reference the ID of the MemberCustomField object itself
    - If the association doesn't exist yet, you have to create it with a POST request. If this is the case,
        you need to reference the related custom field.
    """

    userObject: EasyVereinReference | Member | None = None
    customField: EasyVereinReference | CustomField | None = None
    value: str | None = None
    requestedValue: str | None = None  # Purpose of this field is not documented


class MemberCustomFieldCreate(
    MemberCustomField, required_mixin(["customField", "value"])
):
    """
    Pydantic model for creating a new member
    """


class MemberCustomFieldUpdate(MemberCustomField):
    """
    Pydantic model used to update a member
    """

    pass


from .custom_field import CustomField  # noqa: E402
from .member import Member  # noqa: E402
