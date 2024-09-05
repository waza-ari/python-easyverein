[![Documentation Status](https://readthedocs.org/projects/python-easyverein/badge/?version=latest)](https://python-easyverein.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
![GitHub issues](https://img.shields.io/github/issues/waza-ari/python-easyverein)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/waza-ari/python-easyverein)
![GitHub top language](https://img.shields.io/github/languages/top/waza-ari/python-easyverein)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/waza-ari/python-easyverein/main.svg)](https://results.pre-commit.ci/latest/github/waza-ari/python-easyverein/main)



# Python EasyVerein

**Full documentation** is [available at Read The Docs](https://python-easyverein.readthedocs.io/en/stable/)

This package contains an unofficial API client for [EasyVerein](http://easyverein.com) written in Python. Please note that this
library is unofficial and therefore not supported in any way by SD Software Design GmbH. If you have issues using this
library, please do not open a support request within EasyVerein but report it to our GitHub repository instead.

## State of the API

This client was written against and tested against the Hexa v1.7 API version of EasyVerein. It may or may not work
with newer / older API versions, so please use them at your own risk. As the EasyVerein API does not expose model
information, the models used as part of this library are specific to this library and are based on information obtained
from the API responses (e.g. required fields when creating an item).

In addition to the official endpoints, the client provides some convenience functions that are not included in the
official API (e.g. setting a custom field of a member to certain value, no matter if it has been set before or not
or create an invoice with items in one go) which makes it much simpler to work with the API.

Not all endpoints offered by the EasyVerein API are supported. For now, only the following endpoints are implemented.
When saying CRUD, it means the library supports various methods to **C**reate, **R**ead, **U**pdate and
**D**elete objects. See the API reference for details on supported CRUD operations.

* `contact-details`: CRUD, Soft-Delete
* `custom-fields`: CRUD, Soft-Delete
* `invoice`: CRUD, Soft-Delete, plus some convenience methods
* `invoice-item`: CRUD
* `member`: CRUD, Soft-Delete
* `member-groups`: CRUD, Soft-Delete
* `member/<id>/custom-fields`: CRUD, plus some convenience methods
* `member/<id>/member-groups`: CRUD, plus some convenience methods
* `wastebasket` (its the official name used by the EasyVerein API to reference soft-deleted objects)

In addition to that, the library supports nested queries using the query syntax, included nested model validation.
See the Usage section of this documentation for more details.

## Installation

Install the package using `poetry`:

```bash
poetry add python-easyverein
```

or `pip`:

```bash
pip install python-easyverein
```

## Getting Started

This simple example shows how to setup the library and retrieve all invoices:

```python
import os
from easyverein import EasyvereinAPI

api_key = os.getenv('EV_API_KEY', '')

ev_client = EasyvereinAPI(api_key)

print(ev_client.invoice.get())
```

The result will be a list of invoice objects. All returned objects are [Pydantic](https://pydantic.dev) models under
the hood, so you get auto-completion and a guaranteed interface for these models. For details please refer to the usage
section of this documentation.

## Tests

All features of this client are automatically tested against the actual API using pytest. If you want to run the tests
yourself, it is advisable to create a separate demo account for that. Then, set the following environment variable to
your API token and simply run `pytest`:

```
EV_API_KEY=<your-api-key>
```

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
