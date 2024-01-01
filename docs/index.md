# Getting Started

Welcome to the documentation for `python-easyverein`, an **unoffical** Python library for the API offered by
[EasyVerein](https://easyverein.com). Please note that this library is unofficial and therefore not supported
in any way by SD Software Design GmbH. If you have issues using this library, please do not open a support request
within EasyVerein but report it to our GitHub repository instead.

## State of the API

This client was written against and tested against the Hexa v1.7 API version of EasyVerein. It may or may not work
with newer / older API versions, so please use them at your own risk. As the EasyVerein API does not expose model
information, the models used as part of this library are specific to this library and are based on information obtained
from the API responses (e.g. required fields when creating an item).

In addition to the official endpoints, the client provides some convenience functions that are not included in the 
official API (e.g. setting a custom field of a member to certain value, no matter if it has been set before or not)
which makes it much simpler to work with the API. These functions contain a hint in the documentation.

Not all endpoints offered by the EasyVerein API are supported. For now, only the following endpoints are implemented:

* `invoice`
* `invoice-item`
* parts of `member`
* `wastebasket` (its the official name used by the EasyVerein API to reference soft-deleted objects. See XXX for details)

## Getting Started

This simple example shows how to setup the library and retrieve all invoices:

```python
import os
from easyverein import EasyvereinAPI

api_url = os.getenv('EV_API_URL', 'https://hexa.easyverein.com/api/')
api_version = os.getenv('EV_API_VERSION', 'v1.7')
api_key = os.getenv('EV_API_KEY', '')

ev_client = EasyvereinAPI(
    api_key,
    base_url=api_url,
    api_version=api_version
)

print(ev_client.invoice.get())
```

The result will be a list of invoice objects. All returned objects are [Pydantic](https://pydantic.dev) models under
the hood, so you get auto completion and a guaranteed interface for these models. For details please refer to the usage
section of this documentation.

## Queries and nested models

By default, the EasyVerein returns references as URL to the linked resource, for example:

`GET {{base_url}}{{api_version}}/invoice/{{invoice_number}}` returns:

```json
{
  "id": 183495599,
  "relatedAddress": "https://hexa.easyverein.com/api/v1.7/contact-details/113185254",
  "model": "Invoice"
}
```

In this case, this library will simply return the same URL as model attribute. The EasyVerein API supports a query
syntax to select the fields you want to return. It also allows you to specify nested fields like this:

```python
invoices = ev_client.invoice.get(
    query="{id,date,dateItHappend,receiver,relatedAddress{id,street,zip}}"
)
```

This query will return the following raw JSON, as will get the specified fields from the `Invoice` itself, but also
select certain fields from the `relatedAddress` associated to it.

```json
{
    "id": 183495599,
    "relatedAddress": {
        "id": 113185254,
        "street": "Warner-Allee 1",
        "zip": "46244"
    },
    "date": "2023-11-28",
    "dateItHappend": "2023-11-26",
    "receiver": "Herr Max Mustermann\nWarner-Allee 1\n46244 Bottrop\nDeutschland"
}
```

In these cases the library automatically contructs nested objects, so you can easily access the nested objects
(including auto completion powered by Pydantic) like this:

```python
for invoice in invoices:
    print(invoice.relatedAddress.street)
```
