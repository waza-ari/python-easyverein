from easyverein import EasyvereinAPI
from rich import print

from easyverein.models.member import MemberFilter

api = EasyvereinAPI("36085a032c5c832596bebe2ad48513e7cad8d5e2")

invoices = api.custom_field.get(limit=50)
print(invoices)