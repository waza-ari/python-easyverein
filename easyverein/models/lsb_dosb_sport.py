from .base import EasyVereinBase
from .mixins.empty_strings_mixin import EmptyStringsToNone


class LsbDosbSport(EasyVereinBase, EmptyStringsToNone):
    """
    Pydantic Model for a LSB/DOSB Sport.
    """

    title: str | None = None
    sportNumber: str | None = None
    federationNumber: str | None = None
