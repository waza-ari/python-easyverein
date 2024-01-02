from .contact_details import ContactDetails, ContactDetailsCreate, ContactDetailsUpdate
from .invoice import Invoice, InvoiceCreate, InvoiceUpdate
from .invoice_item import InvoiceItem, InvoiceItemCreate, InvoiceItemUpdate
from .member import Member, MemberCreate, MemberUpdate

ContactDetails.model_rebuild()
Invoice.model_rebuild()
InvoiceItem.model_rebuild()
Member.model_rebuild()
