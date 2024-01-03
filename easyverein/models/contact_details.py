"""
Contact Details related models
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from ..core.types import Date, Email
from .base import EasyVereinBase
from .mixins.required_attributes import required_mixin


class ContactDetails(EasyVereinBase):
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
    privateEmail: Email | None = None
    companyEmail: Email | None = None
    companyEmailInvoice: Email | None = None
    primaryEmail: str | None = "email"
    preferredEmailField: Literal[0, 1, 2] | None = Field(
        default=None, alias="_preferredEmailField"
    )
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
    additionalAdressInfo: str | None = Field(
        default=None, max_length=128
    )  # Intentionally written wrong, as per API
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
    sepaDate: Date | None = None
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


class ContactDetailsUpdate(ContactDetails):
    """
    Pydantic model used to update contact details
    """

    isCompany: bool | None = Field(default=None, serialization_alias="_isCompany")
    preferredEmailField: Literal[0, 1, 2] | None = Field(
        default=None, alias="_preferredEmailField"
    )


class ContactDetailsCreate(ContactDetailsUpdate, required_mixin(["isCompany"])):
    """
    Pydantic model for creating new contact details
    """
