# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`python-easyverein` is an unofficial Python client for the [EasyVerein](http://easyverein.com) v2.0 REST API. It is published to PyPI as `python-easyverein` and imported as `easyverein`. All API objects are returned as validated Pydantic v2 models. The library is not affiliated with EasyVerein — report problems to this repo, not to EasyVerein support.

## Commands

The project uses [Task](https://taskfile.dev) (`Taskfile.yml`) over Poetry. Common workflows:

- `task lint` — `ruff check easyverein --fix` then `ruff format easyverein`
- `task typecheck` — `mypy easyverein`
- `task test` — `pytest`
- `task all` — lint, typecheck, then test (run this before considering work done)
- `task docs` — serve mkdocs locally
- `task release VERSION=X.Y.Z` — bumps version in `pyproject.toml` and `easyverein/__init__.py`, commits, tags, and pushes (releases are also done via this task by the maintainer)

Run a single test: `poetry run pytest tests/test_invoice.py::TestInvoices::test_get_invoices`

### Tests require a live API

There are **no mocks** — the entire `tests/` suite runs against a real EasyVerein tenant. Set `EV_API_KEY` (read via `pytest-dotenv` from `.env`, or as an env var) to a **dedicated demo account**, not a production one, because tests create and delete real objects. Tests assume specific seeded example data (e.g. `test_get_invoices` asserts exactly 6 invoices exist). `tests/unit/` is the only mock-free-but-offline portion (pure model validation and v2/v3 name translation). Set `EV_API_VERSION=v3.0` to run the live suite against v3.0; never run both versions concurrently against the same tenant.

## Architecture

The codebase has three parallel layers, one file per API resource in each. To add or change an endpoint you usually touch all three:

1. **`easyverein/models/`** — Pydantic models describing API resources. Each resource defines a family of classes following a strict naming convention: a `XYZBase` with all fields, then `XYZ` (read/representative), `XYZCreate`, `XYZUpdate`, and `XYZFilter`. These are re-exported from `easyverein/models/__init__.py`.

2. **`easyverein/modules/`** — one `XYZMixin` per resource (e.g. `InvoiceMixin`). Each mixin composes generic CRUD behavior plus any resource-specific convenience methods (e.g. `InvoiceMixin.create_with_items`, `create_with_attachment`).

3. **`easyverein/api.py`** — `EasyvereinAPI`, the single public entry point. Its constructor instantiates every mixin and exposes them as attributes (`api.invoice`, `api.member`, `api.booking`, …). Usage is always `EasyvereinAPI(api_key).<resource>.<method>(...)`.

### Generic CRUD via mixins

Shared behavior lives in `easyverein/modules/mixins/`:

- `crud.py` — `CRUDMixin[Model, Create, Update, Filter]` (get / get_all / get_by_id / create / update / delete) and `BulkUpdateCreateMixin` (bulk_create / bulk_update, only for endpoints the API supports it on).
- `recycle_bin.py` — `RecycleBinMixin` (`get_deleted`, `purge`) for the API's soft-delete "wastebasket".

A resource mixin is wired up by subclassing the generic mixins with concrete type parameters and setting four instance attributes in `__init__`: `endpoint_name`, `return_type`, `self.c` (client), `self.logger`. The generic mixins rely on `EVClientProtocol` (`core/protocol.py`) to access these attributes in a type-safe way.

`get` returns one page as `(list, total_count)`; `get_all` transparently follows pagination. `delete(..., delete_from_recycle_bin=True)` soft-deletes then purges (two API calls).

### HTTP client

`easyverein/core/client.py` (`EasyvereinClient`) is the single layer that talks HTTP via `requests`. It builds URLs, attaches the bearer token, serializes Pydantic models (`model_dump(exclude_none=..., exclude_unset=True, by_alias=True)`), and parses responses into `ResponseSchema` (`core/responses.py`). It handles:

- **429 rate limiting** — honors `Retry-After`; sleeps and retries only if `auto_retry=True`, otherwise raises `EasyvereinAPITooManyRetriesException`.
- **Token refresh** — when the API sets the `tokenRefreshNeeded` (v3.0: `token_refresh_needed`) header, `EasyvereinAPI.handle_token_refresh()` fires; with `auto_refresh_token=True` it calls `/refresh-token` and swaps the in-use key. A `token_refresh_callback` lets callers persist the new `BearerToken`.

### API versions (v2.0 and v3.0)

Both API versions are supported with **one set of models**; `api_version` defaults to `v2.0` (v1.7 is rejected). v3.0 renamed every field, filter and query name to snake_case, so the Python attribute names stay the v2.0 names and the translation happens on the wire:

- `core/api_version.py` — naming rules (`to_snake_case`, `translate_query`), version-specific parameter / header names (`COUNT_PARAM`, `TOKEN_REFRESH_HEADER`).
- `models/mixins/versioned.py` — `VersionedModel` (base of `EasyVereinBase`, `EasyVereinFilter` and action models) renames keys in a before-validator and a wrap serializer when the Pydantic context contains `{"api_version": "v3.0"}`. Exceptions to the derived snake_case name go into a `__v3_names__` class dict (`None` = unsupported in v3.0, e.g. the `deleted` filter).
- The client passes that context everywhere: always serialize via `client.serialize()`, build list URLs via `client.list_params()`, translate `query` strings via `translate_query()` and parse via `parse_models(..., self.c.context)`.
- Sub endpoints that v3.0 turned into top level endpoints (member custom fields, member groups, select options) switch `endpoint_name` per version, scope list requests via the `scope_params` property and inject the parent reference on `create`.

The v3.0 changelog is unreliable (see `KNOWN_ISSUES.md`); verify filter names against the `parameters` of the v3.0 OpenAPI spec embedded in the HTML documentation, which matched the live API.

### Custom field types

`easyverein/core/types.py` holds the Annotated Pydantic types that encode API quirks: `EasyVereinReference` (a field can be either an `int` id *or* a full URL), `Date`/`DateTime` with API-specific serialization formats, and `FilterIntList`/`FilterStrList` which serialize lists to comma-separated strings for query filters.

### Model conventions and API quirks

- **Underscore-prefixed API fields**: the API uses many `_fieldName` attributes. Pydantic treats leading underscores as private, so models expose the normalized name (`isCompany`) mapped via a `Field(alias="_isCompany")`. Read this name when accessing parsed objects. `Create`/`Update` variants use `serialization_alias` only. See `KNOWN_ISSUES.md` for the full rationale.
- **`required_mixin([...])`** (`models/mixins/required_attributes.py`) is a class factory that adds a Pydantic validator enforcing required fields on `Create` models. List elements that are themselves lists mean "at least one of these must be set" (e.g. invoice needs `relatedAddress` *or* `receiver`).
- **`EmptyStringsToNone`** (`models/mixins/empty_strings_mixin.py`) rewrites empty strings the API sometimes returns into `None` before validation.

**Always check `KNOWN_ISSUES.md` before touching models** — it documents upstream API bugs the client works around (empty-string `path`, invoice draft-state 500s, member custom-field deletion behavior, etc.).

### Filter generation

`dev/generate_filter.py` generates the `XYZFilter` Pydantic field definitions from an EasyVerein swagger spec (`dev/api/<version>.json`). Filters are not hand-maintained from scratch — regenerate from the v2.0 spec when the API changes and add `__v3_names__` overrides where the v3.0 name is not the snake_case version of the v2.0 name.

## Conventions

- Linting/formatting is `ruff` (line length 120); type checking is `mypy`. A `pre-commit` config is provided and runs in CI.
- Python 3.11+ (`requires-python = ">=3.11,<4"`).
- Documentation is mkdocs + mkdocstrings (`docs/`, published to Read the Docs); docstrings use the NumPy convention and are part of the public docs, so keep them accurate.
