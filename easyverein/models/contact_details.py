"""
Contact Details related models
"""
from __future__ import annotations

from typing import Literal, Any

from pydantic import BaseModel, PositiveInt, Field, EmailStr

from ..core.types import Date, EasyVereinReference
from .mixins.required_attributes import required_mixin


class ContactDetails(BaseModel):
    """
    Pydantic model representing contact details

    Note that contact details can be created standalone (independently of members), but members
    are required to have a contact details linked.
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None
    # TODO: Add reference to Organization once implemented
    _deleteAfterDate: Date | None = None
    _deletedBy: str | None = None
    _isCompany: bool | None = None
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
    # Hint: 0 = Same as login, 1 = private, 2 = company
    _preferredEmailField: Literal[0, 1, 2] | None = None
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
    sepaDate: Date | None = None
    # Hint: 0 = not selected, 1 = direct debit, 2 = bank transfer, 3 = cash, 4 = Other
    methodOfPayment: int | None = None
    datevAccountNumber: int | None = None
    _copiedFromParent: Any | None = None  # TODO: Refine once available from API description
    _copiedFromParentStartDate: Any | None = None  # TODO: Refine once available from API description
    _copiedFromParentEndDate: Any | None = None  # TODO: Refine once available from API description
    _copiedFromParentEndDateAction: Any | None = None  # TODO: Refine once available from API description


class ContactDetailsCreate(ContactDetails, required_mixin(["contactDetails"])):
    """
    Pydantic model for creating a new member
    """


class ContactDetailsUpdate(ContactDetails):
    """
    Pydantic model used to update a member
    """

    pass
