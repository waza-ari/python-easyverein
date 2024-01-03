from pydantic import BaseModel, Field, PositiveInt

from ..core.types import DateTime, EasyVereinReference


class EasyVereinBase(BaseModel):
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
