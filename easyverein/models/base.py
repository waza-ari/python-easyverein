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
    deletedBy: str | None = Field(default=None, alias="_deletedBy")
