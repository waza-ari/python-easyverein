| API Endpoint | Namespace                   | Supported Generics  |
|--------------|-----------------------------|---------------------|
| `invoice`    | `evclient.invoice.<method>` | CRUD and RecycleBin |

The `isDraft` attribute of invoices is of particular interest, as many modifications are not permitted
by the API if `isDraft = False`. Also, the endpoint to create endpoints is pretty limited, you cannot
pass invoice items or attachments when creating the invoice object. In general, you'll need to create
the invoice in draft state first, perform the necessary modifications (like adding an attachment or
adding items) and then remove the draft state.

!!! note "Removing the draft state and PDF attachments"
    When removing the draft state (patch the invoice to set `isDraft = False` one of two things) can
    happen:

    - If you uploaded an attachment earlier, the invoice is simply created as is
    - If there's no attachment yet, and the invoice type is set appropriately, EasyVerein automatically
        generates a PDF invoice based on the settings you have configured.

## Additional parameters

None

## Generic Model Mappings

| Generic Model     | Invoice Model   |
|-------------------|-----------------|
| `ModelType`       | `Invoice`       |
| `CreateModelType` | `InvoiceCreate` |
| `UpdateModelType` | `InvoiceUpdate` |

## Additional Methods

::: easyverein.modules.invoice.InvoiceMixin
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