| API Endpoint   | Namespace                        | Supported Generics |
|----------------|----------------------------------|--------------------|
| `custom-field` | `evclient.custom_field.<method>` | CRUD, RecycleBin   |

## Additional parameters

None

## Generic Model Mappings

| Generic Model     | Invoice Model       |
|-------------------|---------------------|
| `ModelType`       | `CustomField`       |
| `CreateModelType` | `CustomFieldCreate` |
| `UpdateModelType` | `CustomFieldUpdate` |

## Additional Methods

::: easyverein.modules.custom_field.CustomFieldMixin
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
