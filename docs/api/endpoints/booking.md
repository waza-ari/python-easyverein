| API Endpoint      | Namespace                           | Supported Generics |
|-------------------|-------------------------------------|--------------------|
| `booking` | `evclient.booking.<method>` | CRUD, RecycleBin   |

## Additional parameters

None

## Generic Model Mappings

| Generic Model     | Invoice Model          |
|-------------------|------------------------|
| `ModelType`       | `Booking`       |
| `CreateModelType` | `BookingCreate` |
| `UpdateModelType` | `BookingUpdate` |

## Additional Methods

::: easyverein.modules.booking.BookingMixin
    options:
        inherited_members: false
        show_signature: true
        show_signature_annotations: true
        show_root_heading: false
        show_bases: false
        show_root_toc_entry: false
        separate_signature: true
        heading_level: 4
        filters:
            - "!^c$"
            - "!^logger$"
            - "!^endpoint_name"
            - "!^return_type"
