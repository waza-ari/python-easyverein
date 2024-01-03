# noqa: F401
from .contact_details import ContactDetails, ContactDetailsCreate, ContactDetailsUpdate
from .custom_field import CustomField, CustomFieldCreate, CustomFieldUpdate
from .invoice import Invoice, InvoiceCreate, InvoiceUpdate
from .invoice_item import InvoiceItem, InvoiceItemCreate, InvoiceItemUpdate
from .member import Member, MemberCreate, MemberUpdate
from .member_custom_field import (
    MemberCustomField,
    MemberCustomFieldCreate,
    MemberCustomFieldUpdate,
)

ContactDetails.model_rebuild()
CustomField.model_rebuild()
Invoice.model_rebuild()
InvoiceItem.model_rebuild()
Member.model_rebuild()
MemberCustomField.model_rebuild()
