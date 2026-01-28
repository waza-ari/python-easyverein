| API Endpoint                       | Namespace                                          | Supported Generics |
|------------------------------------|----------------------------------------------------|--------------------|
| `member/<member_id>/custom-fields` | `evclient.member.custom_fields(<member>).<method>` | CRUD               |

## Additional parameters

As member related custom fields are always bound to a specific member, the namespace used for custom field associations
requires the member as constructor argument, to avoid passing it again to all endpoints:

| Name     | Type    | Description | Default                                                                                           |
|----------|---------|-------------|---------------------------------------------------------------------------------------------------|
| `member` | `Member | int`        | Identifies the member to modify custom field values on. Can be either an id or a `Member` object. | *required* |

## Generic Model Mappings

| Generic Model     | Invoice Model             |
|-------------------|---------------------------|
| `ModelType`       | `MemberCustomField`       |
| `CreateModelType` | `MemberCustomFieldCreate` |
| `UpdateModelType` | `MemberCustomFieldUpdate` |

## Additional Methods

::: easyverein.modules.member_custom_field.MemberCustomFieldMixin
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