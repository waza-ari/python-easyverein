"""
Contact Details related models
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field

from ..core.types import Date, DateTime, FilterIntList
from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin


class ContactDetailsBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `ContactDetails` | `ContactDetailsUpdate` | `ContactDetailsCreate` |

    !!! info "Contact Details and Members"
        Note that contact details can be created standalone (independently of members), but members
        are required to have a contact details object linked.
    """

    isCompany: bool | None = Field(default=None, alias="_isCompany")
    """Alias for `_isCompany` field. See [Pydantic Models](../usage.md#pydantic-models) for details."""
    salutation: Literal["", "Herr", "Frau"] | None = None
    firstName: str | None = Field(default=None, max_length=128)
    familyName: str | None = Field(default=None, max_length=128)
    nameAffix: str | None = Field(default=None, max_length=100)
    dateOfBirth: Date | None = None
    internalNote: str | None = None
    privateEmail: EmailStr | None = None
    companyEmail: EmailStr | None = None
    companyEmailInvoice: EmailStr | None = None
    primaryEmail: str | None = "email"
    preferredEmailField: Literal[0, 1, 2] | None = Field(default=None, alias="_preferredEmailField")
    """
    Alias for `_preferredEmailField` field. See [Pydantic Models](../usage.md#pydantic-models) for details.

    Possible values:

    - 0: same as login
    - 1: private
    - 2: company
    """
    # Hint: 0 = mail, 1 = phone, 3 = no communication
    preferredCommunicationWay: Literal[0, 1, 2] | None = None
    companyName: str | None = None
    invoiceCompany: bool | None = None
    sendInvoiceCompanyMail: bool | None = None
    addressCompany: bool | None = None
    privatePhone: str | None = Field(default=None, max_length=100)
    companyPhone: str | None = Field(default=None, max_length=100)
    mobilePhone: str | None = Field(default=None, max_length=100)
    street: str | None = Field(default=None, max_length=128)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=64)
    additionalAdressInfo: str | None = Field(default=None, max_length=128)  # Intentionally written wrong, as per API
    zip: str | None = Field(default=None, max_length=20)
    country: str | None = Field(default=None, max_length=50)
    companyStreet: str | None = Field(default=None, max_length=100)
    companyCity: str | None = Field(default=None, max_length=64)
    companyState: str | None = Field(default=None, max_length=100)
    companyZip: str | None = Field(default=None, max_length=20)
    companyCountry: str | None = Field(default=None, max_length=50)
    professionalRole: str | None = Field(default=None, max_length=500)
    balance: float | None = None
    iban: str | None = Field(default=None, max_length=50)
    bic: str | None = Field(default=None, max_length=100)
    bankAccountOwner: str | None = Field(default=None, max_length=128)
    sepaMandate: str | None = Field(default=None, max_length=60)
    sepaDate: DateTime | None = None
    methodOfPayment: int | None = None
    """
    Defines the method of payment preferred by the user.

    Possible values:

    - 0: not selected
    - 1: direct debit
    - 2: bank transfer
    - 3: cash
    - 4: other
    """
    datevAccountNumber: int | None = None
    # TODO: Refine once available from API description
    copiedFromParent: Any | None = Field(default=None, alias="_copiedFromParent")
    """
    Alias for `_copiedFromParent` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    # TODO: Refine once available from API description
    copiedFromParentStartDate: Any | None = Field(
        default=None,
        alias="_copiedFromParentStartDate",
    )
    """
    Alias for `_copiedFromParentStartDate` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    # TODO: Refine once available from API description
    copiedFromParentEndDate: Any | None = Field(
        default=None,
        alias="_copiedFromParentEndDate",
    )
    """
    Alias for `_copiedFromParentEndDate` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """
    # TODO: Refine once available from API description
    copiedFromParentEndDateAction: Any | None = Field(
        default=None,
        alias="_copiedFromParentEndDateAction",
    )
    """
    Alias for `_copiedFromParentEndDateAction` field. See [Pydantic Models](../usage.md#pydantic-models) for details.
    """


class ContactDetails(ContactDetailsBase, EmptyStringsToNone):
    """
    Pydantic model for contact details
    """

    pass


class ContactDetailsUpdate(ContactDetailsBase):
    """
    Pydantic model used to update contact details
    """

    isCompany: bool | None = Field(default=None, serialization_alias="_isCompany")
    preferredEmailField: Literal[0, 1, 2] | None = Field(default=None, alias="_preferredEmailField")


class ContactDetailsCreate(ContactDetailsUpdate, required_mixin(["isCompany"])):  # type: ignore
    """
    Pydantic model for creating new contact details
    """


class ContactDetailsFilter(BaseModel):
    """
    Pydantic model used to filter contact details
    """

    id__in: FilterIntList | None = None
    country: str | None = None
    isCompany: bool = Field(default=None, serialization_alias="_isCompany")
    preferredCommunicationWay: str | None = None
    contactDetailsGroups: str | None = None
    contactDetailsGroups__not: str | None = None
    dateOfBirthUnset: bool | None = None
    showBirthdaysBetween: str | None = None
    deleted: bool | None = None
    firstName: str | None = None
    familyName: str | None = None
    companyName: str | None = None
    isReferencedByOrgUser: bool | None = None
    lat: str | None = None
    lng: str | None = None
    hasCopyInOrg: str | None = None
    hasCopyInOrg__not: str | None = None
    isCopy: bool | None = None
    hasCopy: bool | None = None
    ordering: str | None = None
    search: str | None = None
