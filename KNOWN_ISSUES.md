# Known Issues

There are some issues on the EV API that we cannot fix on API client side. They're documented
here so we can track them and remove when fixed on EV side

## Invoices

- The `path` attribute of `Invoice` is supposed to be a reference or `None`, but sometimes returns an emptry string. For this purpose, we've implemented the `empty_string_to_none` validator and added it as `BeforeValidator` to rewrite emptry strings to None before performing URL parsing.
- The API returns a 500 Internal Server Error when trying to remove the Draft state (`isDraft=False`), where the `taxRate` or `gross` setting doesn't match between `Invoice` and `InvoiceItem`
