| API Endpoint                       | Namespace                                          | Supported Generics |
|------------------------------------|----------------------------------------------------|--------------------|
| `custom-field/<custom_field_id>/select-options` | `evclient.custom_field.select_options(<custom_field>).<method>` | CRUD               |

## Additional parameters

As select options are always bound to a specific custom field, the namespace used for the select options
requires the custom field or its ID as constructor argument, to avoid passing it again to all endpoints:

| Name     | Type    | Description | Default                                                                                           |
|----------|---------|-------------|---------------------------------------------------------------------------------------------------|
| `custom_field_id` | `CustomField | int`        | Identifies the custom field to modify select options for. Can be either an id or a `CustomField` object. | *required* |

## Generic Model Mappings

| Generic Model     | CustomFieldSelectOption Model   |
|-------------------|---------------------------|
| `ModelType`       | `CustomFieldSelectOption`       |
| `CreateModelType` | `CustomFieldSelectOptionCreate` |
| `UpdateModelType` | `CustomFieldSelectOptionUpdate` |

## Additional Methods

::: easyverein.modules.custom_field_select_option.CustomFieldSelectOptionMixin
    options:
        inherited_members: false
        show_signature: true
        show_signature_annotations: true
        show_root_heading: false
        show_bases: false
        show_root_toc_entry: false
        separate_signature: true
        heading_level: 3
        filters:
            - "!^c$"
            - "!^logger$"
            - "!^endpoint_name"
            - "!^return_type"