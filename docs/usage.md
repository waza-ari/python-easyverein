# Usage

## Creating a client object

Before you can do any requests, you'll need to create the client object first. The signature is as follows:

```python
EasyvereinAPI(
    api_key,
    api_version="v1.7",
    base_url="https://easyverein.com/api/",
    logger=None,
)
```

The only mandatory parameter is the `api_key`, which you can get from your EasyVerein portal. It is not recommended
to change `api_version` or `base_url`, as the default values are the values this library is written and tested against.
You can optionally specify your own Python `logger`, see the logging section below.

!!! info "Authentication"
    While the EasyVerein API also supports making requests with a user scoped token, this is not officially
    documented anywhere and would also require the username and password of the specified user. Therefore, only
    the org token that is displayed in the Portal is supported.

Once you have the client object, all supported attributes are composed into the client as instance attributes

```python
from easyverein import EasyvereinAPI

c = EasyvereinAPI(api_key="your_key")

# Get invoices
invoices, total_count = c.invoice.get()
invoices = c.invoice.get_all()

# Members
c.member.get()
```

The available endpoints are documented in the API Reference section of this documentation.

## Handling Token Refresh

Starting version v2.0, the EasyVerein API enforces token expiration. The token you get from
the API configuration page is only valid for 30 days and must be refreshed afterwards. This library is not
responsible for storing the token, but you can pass a callback function that will be called if a token refresh
is needed. Optionally, you can instruct the library to automatically refresh the token for you and pass it to the
callback function.

!!! info "Version 2.0 only"
    Please not that the new token type is only supported in API version 2.0. If you're using API version 1.7, you
    do not need to configure token refresh, the library will raise an exception if you try.

There are two ways this can be done, one synchronous and one asynchronous option. When using asynchronously,
the callback will be called without any arguments, just a a trigger for you to refresh and store the token somewhere
else, for example using an async worker. It does not extend the runtime of the initial request.

```python
from easyverein import BearerToken, EasyvereinAPI

def handle_token_refresh() -> None:
    # This merely serves as a trigger for you to refresh and store the token
    return None

c = EasyvereinAPI(api_key="your_key", api_version="v2.0", token_refresh_callback=handle_token_refresh)
```

The more convenient way is to use the automatic token refresh. This will automatically refresh the token for you and
pass it to the callback for you to store. It does so after the initial request is completed (as this is needed to get
the feedback from the API in the first place) but before the result is returned. It therefore extends the runtime of
the request by a small amount, which may or may not be acceptable for your use case.

```python
from easyverein import BearerToken, EasyvereinAPI

def handle_token_refresh(new_token: BearerToken) -> None:
    print(f"New token: {new_token.Bearer}")
    return None

c = EasyvereinAPI(
    api_key="your_key",
    api_version="v2.0",
    token_refresh_callback=handle_token_refresh,
    auto_refresh_token=True
)
```

## Pydantic Models

All interactions with the API are handled by using Pydantic (v2) models. They do the heavy lifting in terms of
parsing (JSON API response to models), validating (make sure all fields adhere to the correct format) and serialization
(convert model back to JSON). For each supported endpoint, there's at least three models provided:

- The **Model** itself (e.g. `Invoice`, `Member`, `CustomField`, ...): These models are used when parsing the API
  responses. As queries (see below) can be used to filter the fields that are returned by the API, all fields of these
  models must be optional by design, but they will perform basic type conversion (e.g. date or datetime strings will
  be parsed into respective `datetime.date` or `datetime.datetime` models). Nested models are automatically resolved,
  too (see below).
- The **CreateModel** (e.g. `InvoiceCreate`, `MemberCreate`, `CustomFieldCreate`): These models are used when creating
  resources. They're usually derived from the Model, but have certain attributes set to be mandatory. Unfortunately
  the official documentation doesn't highlight which attributes are required in most cases, so for those models it's
  based on experiments conducted by the author.
- The **UpdateModel** (e.g. `InvoiceUpdate`, `MemberUpdate`, `CustomFieldUpdate`): These models are used when modifying
  an existing resource. In most cases they're simply derived from the Model without any changes, as all attributes are
  optional (as a `PATCH` request can be used to change a single field only).

!!! info "Underscore Prefixed Attributes"
    The API spec contains attributes prefixed by underscores (`_isApplication`, `_deletedBy`). In addition, these
    underscored attributes are not used consistently (most of them indicate that the attribute might be read only,
    but that doesn't appply to all of them). Pydantic [does not treat private attributes as Fields](https://docs.pydantic.dev/latest/concepts/models/). 
    
    That means setting them directly is not supported. As a workaround, we're using Pydantic
    [Field Aliases](https://docs.pydantic.dev/latest/concepts/fields/#field-aliases), which means you can access and
    define them without underscore (`_isApplication` simply becomes `isApplication` and this library takes care about
    proper serialization towards the API.

    ??? note "Technical Details"

        We need to use the alias both when parsing the API reply (e.g. into `ContactDetails` model), as well as during
        serialization. It is not possible to access the parsed result using the alias, so the user has to use the
        normalized name (`isCompany` instead of `_isCompany`) when accessing the parsed attribute.

        Without further measures, the user would need to supply `_isCompany` when creating a model though, as this
        technically is a validation, too. Therefore we overwrite the "private" attributes in the `XYZCreate`
        and `XYZUpdate` models using only a `serialization_alias`, to keep the user experience consistent.

        In summary this means:

        - The `Model` itself uses an alias to map the attribute both for validation and serialization. This means
          the model can properly parse an API response. While it is not usually used for serialization, it doesn't
          hurt to configure it. In the client code, the user can access the attribute using the non-prefixed name
        - The `CreateModel` and `UpdateModel` inherits from the `Model` but overwrites the prefixed attributes. Here,
          only the serialization alias is set. This way, the user can create the object using the non-prefixed name,
          the same way it is usually accessed while style providing proper serialization.

## Reading Data

### Supported GET methods

To read data from the API, all CRUD endpoints feature the `get`, `get_all` and `get_by_id` endpoints.

- `get()`: Returns a single page of the resource and the total count
- `get_all()`: Provides an abstraction layer around pagination, fetches all available resources
- `get_by_id`: Returns a single resource based on its resource id

All responses are parsed by the respective Pydantic model, therefore you can access attributes using a well-defined
API including auto-completion and type hinting by popular IDEs.

**Example**:

```python
# get() returns the member and total count
members, total_count = ev_connection.member.get()

# Get all returns a simple list, you can obtain the total count based on the list length
invoices = ev_connection.invoice.get_all(limit_per_page=100)

# Invoices now is a list of Invoice objects
for invoice in invoices:
    print(invoice.isDraft)
    print(invoice.invNumber)
```

### Using filters

The library also supports using the search parameters and filters, on the `get()` and `get_all()` endpoint. For this
to work, you need to define a filter model and pass it as parameter. The filter model is generated using the OpenAPI
specs provided by the EasyVerein API and validated as Pydantic model, too.

**Example**

```python
search = InvoiceFilter(
    invNumber__in=["1", "3", "5"], canceledInvoice__isnull=True, isDraft=False
)

filtered_invoices, total_count = ev_connection.invoice.get(search=search)
```

### Pagination

The `get_all()` endpoint abstracts the need for pagination from the user, as it will simply fetch all resources of a
given endpoint, potentially by doing multiple API requests. If you need additional control, you can always fall back
to the `get()` method, which accepts two parameters:

- `limit`: elements to be returned per page
- `page`: page to return

This endpoints are passed to the query string without validation, so please make sure to stay within the limits
imposed by the EV API.

### The `get()` Endpoint and total count`

The `get()` method returns a tuple, consisting of the parsed response and the total count in addition. There`s three
possible options on how to work on that:

```python
# If you need both the returned values and the total count, simply unpack them
members, total_count = ev_connection.member.get()

# In case you don't need the total count, the preferred way is to simply access the first element of the response
members = ev_connection.member.get()[0]

# Another common option (although not recommended, because it shadows a function of the popular gettext library)
# is to use `_` as temporary variable:

members, _ = ev_connection.member.get()
```

### EasyVerein References

In many cases, a model can reference other models. For example, the `Invoice` model has a `relatedAddress` attribute. By
detault, the API returns a HTTP link to this model. Consider this partial reply from the `invoice` endpoint as example:


`GET {{base_url}}{{api_version}}/invoice/{{invoice_number}}` returns:

```json
{
  "id": 183495599,
  "relatedAddress": "https://easyverein.com/api/v1.7/contact-details/113185254",
  "model": "Invoice"
}
```

This default behaviour changes when nested queries are used, as the same field (`contactDetails`) then contains the
nested fields directly instead of a URL. As a consequence, this library handles this as follows:

- If the returned attribute contains an empty string (`""`), the attribute is set to `None`
- If the returned attribute is any other string, it is validated as HTTP Url
- If the returned attribute is a dictionary, it is parsed and validated as nested model

### Queries and nested models

The EasyVerein API supports a query syntax to select the fields you want to return. It also allows you to specify
nested fields like this:

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

Example with multiple nesting levels. For each member, this example will print all groups the member is assigned to:

```python
allmembers = ev_client.member.get_all(
    query="{membershipNumber,contactDetails{familyName,firstName,dateOfBirth},memberGroups{memberGroup{short}}}"
)
for m in allmembers:
    print(f"{m.membershipNumber} {m.contactDetails.familyName} {m.contactDetails.firstName} {m.contactDetails.dateOfBirth}")
    if m.memberGroups is not None:
        for g in m.memberGroups:
            print(f"     Group: {g.memberGroup.short}")
```

## Creating Resources

The CRUD endpoints support creating objects and offer accompanying model types to facilitate type checking and rough
consistency checking. Note that the EasyVerein API and its documentation does not expose information about required
attributes, so the checks are solely based on information obtained from experiments.

Minimal example:

```python
from easyverein import EasyvereinAPI
from easyverein.models import CustomFieldCreate

ev_client = EasyvereinAPI("<your-token>")

custom_field_model = CustomFieldCreate(
    name="Test-Field",
    kind="e",
    settings_type="t"
)
response = ev_client.custom_field.create(custom_field_model)

# Response now has type CustomField and contains the parsed response from the API
```

## Updating Resources

Resources can be changed (patched) by using the appropriate update model. All the attributes are optional, as single
fields can be patched without any issues. The resource to update can either be identified by a model or its id, 
whatever is more convenient for you.

```python
from easyverein import EasyvereinAPI
from easyverein.models import CustomFieldUpdate

ev_client = EasyvereinAPI("<your-token>")

custom_field_id = 123456

# We cant to change the name
update_model = CustomFieldUpdate(
    name="New Name"
)

# We can either update the model
custom_field = ev_client.custom_field.get_by_id(custom_field_id)
ev_client.custom_field.update(
    custom_field,
    update_model
)

# Alternatively, we can use the ID only
ev_client.custom_field.update(
    custom_field_id,
    update_model
)
```

## Deleting Resources

Depending on the resource type (endpoint), resources can be deleted immediately or are soft-deleted. If they're
soft-deleted, they're not gone. Instead, they're placed in a recycle bin (the official API spec calls this
"wastebasket"). This means that they're not returned by normal query operations, but otherwise are still in the
database and are considered when checking for attribute uniqueness (e.g. `Invoice.invNumber` must be unique and
includes soft-deleted objects in the check).

The delete operation either takes the model to be deleted or its ID as argument. If the endpoint supports the
soft-delete pattern, it also takes a second argument that can be used to immediately purge the element.

Example:

```python
from easyverein import EasyvereinAPI

ev_client = EasyvereinAPI("<your-token>")

invoice_id = 123456

# We can either update the model
invoice = ev_client.invoice.get_by_id(invoice_id)

# Delete the model by using the model. Will soft-delete by default
ev_client.invoice.delete(invoice)
# As we didn't fully delete the item, we can view, restore or purge it, see below.

# Alternatively, we can use the model. Also, we set the second parameter to make sure the object gets purged
ev_client.invoice.delete(invoice_id, delete_from_recycle_bin=True)
```

## Dealing with soft-deleted resources

Once resources are soft-deleted (placed in the recycle bin) they are no longer returned using the normal data
fetching methods described above. Instead, this library provides additional methods to work with these objects. They
are only supported on endpoints which make use of the soft-delete pattern.

!!! info "Endpoints supporting soft-delete"
    As of today, only the following endpoints are implemented by this library and support the soft-delete pattern:

    - invoice
    - member
    - contact-details
    - custom-field

For these endpoints, three additional methods are provided. Refer to the API documentation for details.

Example:

```python
from easyverein import EasyvereinAPI

ev_client = EasyvereinAPI("<your-token>")

# Get all soft-deleted invoices
invoices = ev_client.invoice.get_deleted()

# We can either restore them
for invoice in invoices:
    ev_client.invoice.restore(invoice)  # Also accepts the ID, so `invoice.id` would work, too.
    
# Or we can delete them for good
for invoice in invoices:
    ev_client.invoice.purge(invoice)  # Also accepts the ID, so `invoice.id` would work, too.
```

## Logging

This library uses the standard Python logging environment to handle logs. If you don't specify a logger as part of
the library initialization, it will log to a logger named `easyverein`.

The recommended loglevel is `INFO`. If you need more details, you can set the loglevel to `DEBUG`, but be aware that
this will be quite verbose.

Alternatively you can pass your own logger (must be compatible with `logging.Logger`) when creating the client. If you
choose to do so, the library will log using the provided logger. In certain corner cases this might give more control
about logs, but in the vast majority of cases it should be sufficient to use the default logging class and simply
configure the logger as required.
