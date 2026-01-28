# Known Issues

There are some issues on the EV API that we cannot fix on API client side. They're documented
here so we can track them and remove when fixed on EV side

## General

- The API uses a lot of attributes prefixed with an underscore. Pydantic [does not treat private attributes as Fields](https://docs.pydantic.dev/latest/concepts/models/). That's fine for parsing, but when there's a need to set them (`isCompany` on `ContactDetails`) this is currently not supported. As a workaround, we're using Pydantic [Field Aliases](https://docs.pydantic.dev/latest/concepts/fields/#field-aliases) for this purpose. This has a side effect though: we need to use the alias both when parsing the API reply (e.g. into `ContactDetails` model), as well as during serialization. It is not possible to access the parsed result using the alias, so the user has to use the normalized name (`isCompany` instead of `_isCompany`) when accessing the parsed attribute. Without further measures, the user would need to supply `_isCompany` when creating a model though, as this technically is a validation, too. Therefore we overwrite the "private" attributes in the `XYZCreate` and `XYZUpdate` models using only a `serialization_alias`, to keep the user experience consistent.
## Invoices

- The `path` attribute of `Invoice` is supposed to be a reference or `None`, but sometimes returns an emptry string. For this purpose, we've implemented the `empty_string_to_none` validator and added it as `BeforeValidator` to rewrite emptry strings to None before performing URL parsing.
- The API returns a 500 Internal Server Error when trying to remove the Draft state (`isDraft=False`), where the `taxRate` or `gross` setting doesn't match between `Invoice` and `InvoiceItem`
- When deleting invoices, they must be deleted from the recycle bin as well, except when they've `isRequest` set to `True`. Then they'll get deleted immediately and trying to purge them will yield a `404` error.

## Contact Details

- There are a bunch of fields lacking description on the API, therefore they're Any-typed for now: `_copiedFromParent`, `_copiedFromParentStartDate`, `_copiedFromParentEndDate`, `_copiedFromParentEndDateAction`
- Filter spec contains both `_isCompany` and `isCompay`. Only keeping `_isCompany` with serialization alias to stay consistent to other models

## Custom Fields

- The API defines 14 possible values for `kind` when creating custom fields, but only 4 of them are properly described. These four match the four you can also create in the Portal, so no idea what the others are meant for.

## Members

- The API does not offer a simple way to ensure that a custom field is set to a certain value for member. You have to either create (POST) a member_custom_field if the member has no relation to a certain custom field yet, or modify an existing one (PATCH) if there is such a relation. Before modifying a value you therefore have to know if such a relation exists or not.
- When deleting a custom field, the relation between the member and a custom field still stays intact, just with `customField` set to `None`. The tests therefore manually delete member custom field associations before deleting the actual custom field definition to not pollute the test tenant.
- Apparently "path" doesn't mean, that is always will be a HTTP URL. In some cases it has been reported that the path is a local file path, following the `<member_number>_<firstname>_<lastname>/<random_number>_<member_number>-SEPA-Mandat_,,,` syntax. My assumption is that those paths have been used before the introduction of S3 storage on EV side. As I couldn't find any documentation around the naming standard, nor find any information how to actually work with these fields, we're simply adding a string fallback.
- In the filter, `contactDetails__preferredCommunicationWay` is defined as `string` while `contactDetails__preferredCommunicationWay__ne` is defined as number. Considering both to be integers
