# Getting Started

Welcome to the documentation for `python-easyverein`, an **unoffical** Python library for the API offered by
[EasyVerein](https://easyverein.com). Please note that this library is unofficial and therefore not supported
in any way by SD Software Design GmbH. If you have issues using this library, please do not open a support request
within EasyVerein but report it to our GitHub repository instead.

## Installation

Install the package using poetry:

```bash
poetry add python-easyverein
```

or `pip`:

```bash
pip install python-easyverein
```

## Basic Usage

All endpoints that are supported by this library are available as attribute of the `ev_client` you create. While
you can specify the API URL and version, the defaults represent the values the library is written and tested against,
so please only change them if you know what you're doing.

This simple example shows how to setup the library and retrieve all invoices:

```py
import os
from easyverein import EasyvereinAPI

api_key = os.getenv('EV_API_KEY', '')

ev_client = EasyvereinAPI(api_key)

print(ev_client.invoice.get())
```

The result will be a list of invoice objects. All returned objects are [Pydantic](https://pydantic.dev) models under
the hood, so you get auto-completion and a guaranteed interface for these models. For details please refer to the
[Usage section](usage.md) of this documentation.

!!! info "Recommended reading"
    It is **highly recommended** to read the [Usage section](usage.md) of this documentation fully, as the EasyVerein API contains
    some peculiarities that this library tries to work around in a hopefully elegant way.

    The [API reference](api/crud.md) contains important information about the supported endpoints, including the convenience methods
    provided by this library.

    The [model reference](models/base.md) contains important information about the model attributes and their potential values. Most of
    them are not easily available from the EasyVerein documentation, so they might be of use to you.

## API Versions

The library supports the v2.0 and v3.0 versions of the EasyVerein API. It defaults to v2.0, but you can select
v3.0 by passing `api_version="v3.0"` when creating the `EasyvereinAPI` object. The models and methods of this library
are identical for both versions, the differences between the versions (most notably the snake_case field names of
v3.0) are handled by the library. See [API v3.0](usage.md#api-v30) in the usage section for details.

API v1.7 is deprecated and not supported by the 2.x releases of this library. If you still need it, pin the library
to version 1.x.

Note that EasyVerein is often doing breaking changes within an API version, so if you encounter
any issues when using this library in a supported configuration (e.g. library 2.x with EV API v2.0), please raise an issue
here.

Version 2.0 introduced a change to authentication, it does not allow the ephemeral API keys anymore. Instead,
a new type of token is used, which expires after 30 days. Please check the usage section on details how to handle
token expiration.

## State of the API

This client was written against and is tested against the v2.0 and v3.0 API versions of EasyVerein. It does not
work with older API versions. As the EasyVerein API does not expose model
information, the models used as part of this library are specific to this library and are based on information obtained
from the API responses (e.g. required fields when creating an item).

In addition to the official endpoints, the client provides some convenience functions that are not included in the 
official API (e.g. setting a custom field of a member to certain value, no matter if it has been set before or not
or create an invoice with an attachment) which makes it much simpler to work with the API.

Not all endpoints offered by the EasyVerein API are supported. For now, only the following endpoints are implemented.
When saying CRUD, it means the library supports various methods to **C**reate, **R**ead, **U**pdate and **D**elete objects. See the API
reference for details on supported CRUD operations.

* `booking`: CRUD, Bulk Create and Update, Soft-Delete
* `booking-project`: CRUD, Soft-Delete
* `billing-account`: CRUD, Soft-Delete
* `contact-details`: CRUD, Bulk Create and Update, Soft-Delete
* `contact-details-group`: CRUD, Soft-Delete
* `custom-fields`: CRUD, Soft-Delete
* `custom-fields/<id>/select-options` (v3.0: `select-option`): CRUD
* `invoice`: CRUD, Bulk Create and Update, Soft-Delete, plus some convenience methods
* `invoice-item`: CRUD
* `member`: CRUD, Bulk Create and Update, Soft-Delete
* `member-groups`: CRUD, Soft-Delete
* `member/<id>/custom-fields` (v3.0: `member-custom-field-assignment`): CRUD, plus some convenience methods
* `member/<id>/member-groups` (v3.0: `member-group-assignment`): CRUD, plus some convenience methods
* `wastebasket` (its the official name used by the EasyVerein API to reference soft-deleted objects)

In addition to that, the library supports nested queries using the query syntax, included nested model validation.
See the [Usage section](usage.md) of this documentation for more details.

## Tests

All features of this client are automatically tested against the actual API using pytest. If you want to run the tests
yourself, it is advisable to create a separate demo account for that. Then, set the following environment variable to
your API token and simply run `pytest`:

```
EV_API_KEY=<your-api-key>
```

The tests run against API v2.0 by default. Set `EV_API_VERSION=v3.0` to run them against API v3.0. Do not run
both versions in parallel against the same account, as the tests rely on the number of existing objects.

## Contributing

The client is written in pure Python, using `mkdocs` with `mkdocstrings` for documentation. Any changes or
pull requests are more than welcome, but please adhere to the code style:

- Use `ruff` based code linting, formatting and styling
- Use `mypy` for static type checking

A pre-commit hook configuration is supplied as part of the project. You can run them prior to your commit using:

```bash
pre-commit

# Or run them for the entire project
pre-commit run --all-files
```

Please make sure that any additions are properly tested. PRs won't get accepted if they don't have test cases to
cover them.

## Getting Help

Once more, this library is not officially supported by SD Software Design GmbH, the company behind EasyVerein.
If you have troubles, please ask yourself the following questions:

- Is your problem around API usage in general, which endpoint to call, which fields to set to achieve a certain thing?
  Do you have questions around attribute naming, usage, or why the API behaves a certain way? Those questions should be
  directed towards their support, as I cannot help with them.
- is your question around how to use this library, a mistake in the Pydantic models it's using, an error in the library
  code or other questions around this library? Please open a GitHub issue for those questions.
