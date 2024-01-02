# Known Issues

There are some issues on the EV API that we cannot fix on API client side. They're documented
here so we can track them and remove when fixed on EV side

## Invoices

- The `path` attribute of `Invoice` is supposed to be a reference or `None`, but sometimes returns an emptry string. For this purpose, we've implemented the `empty_string_to_none` validator and added it as `BeforeValidator` to rewrite emptry strings to None before performing URL parsing.
- The API returns a 500 Internal Server Error when trying to remove the Draft state (`isDraft=False`), where the `taxRate` or `gross` setting doesn't match between `Invoice` and `InvoiceItem`
- When deleting invoices, they must be deleted from the recycle bin as well, except when they've `isRequest` set to `True`. Then they'll get deleted immediately and trying to purge them will yield a `404` error.

## Contact Details

- There are a bunch of fields lacking description on the API, therefore they're Any-typed for now: `_copiedFromParent`, `_copiedFromParentStartDate`, `_copiedFromParentEndDate`, `_copiedFromParentEndDateAction`