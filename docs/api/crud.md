## Overview

The following methods are common to all endpoints and are therefore only documented once.
All these methods are defined in a generic class and are therefore generically typed. Refer to
the documentation of each endpoint to see the mapping between the generic types and the Pydantic
models for the specific endpoint.

!!! note "Additional parameters"
    Note that some endpoints require additional parameters, which can be mandatory. For example,
    to work with custom field values on members, you need to specify the member id to work with.

    These cases are highlighted as part of the respective endpoint API documentation.

## Generic Classes

- `ModelType`: The pydantic model used for displaying data at the respective endpoint. Usually used
   parse the API response and returned to the user.
- `CreateModelType`: The pydantic model used for creating resources using this endpoint. In some
   cases (where documented on the EasyVerein side) the Pydantic models are enforcing required fields
   when creating resources. As the EasyVerein documentation is incomplete, expect these checks to be
   incomplete, too.
- `UpdateModelType`: Used when patching a certain resource. Patching can be done on single fields,
   therefore all attributes are optional.

## Method Reference

::: easyverein.modules.mixins.crud.CRUDMixin
    options:
        heading_level: 3
        show_signature: true
        show_signature_annotations: true
        show_root_toc_entry: false
        separate_signature: true
