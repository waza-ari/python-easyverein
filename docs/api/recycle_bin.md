## Overview

Some endpoints support a soft-delete pattern, meaning that resources are not immediately deleted. Instead,
they're put into a recycle bin (EasyVerein calls that "wastebasket"). These methods provide a way to interact
with soft-deleted resources.

!!! note "Endpoints supporting soft delete"
    Note that not all endpoints support the soft-delete pattern. Using this Client, only the following
    endpoints are supported for now:

    - invoice
    - member
    - member-groups
    - contact-details
    - custom-field
    
    Please refer to the offical API documentation for a full list endpoints supporting soft-delete.

## Method Reference

::: easyverein.modules.mixins.recycle_bin.RecycleBinMixin
    options:
        heading_level: 3
        show_signature: true
        show_signature_annotations: true
        show_root_toc_entry: false
