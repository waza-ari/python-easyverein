from pydantic import Field, PositiveInt

from ..core.types import DateTime, EasyVereinReference
from .mixins.versioned import VersionedModel


class EasyVereinBase(VersionedModel):
    """
    Base class encapsulating common fields for all models
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None
    # TODO: Add reference to Organization once implemented
    deleteAfterDate: DateTime | None = Field(default=None, alias="_deleteAfterDate")
    """Alias for `_deleteAfterDate` field. See [Pydantic Models](../usage.md#pydantic-models) for details."""
    deletedBy: str | None = Field(default=None, alias="_deletedBy")
    """Alias for `_deletedBy` field. See [Pydantic Models](../usage.md#pydantic-models) for details."""


class EasyVereinFilter(VersionedModel):
    """
    Base class for all filter models.

    Filter attributes use the API v2.0 names and are translated automatically when using API v3.0.
    """

    __v3_names__ = {
        # v3.0 removed the `deleted` filter, use the recycle bin methods (`get_deleted`) instead
        "deleted": None,
    }
