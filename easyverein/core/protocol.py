import logging
from typing import Any, Protocol, Type, TypeVar

from .client import EasyvereinClient

T = TypeVar("T", covariant=True)


# noinspection PyPropertyDefinition
class EVClientProtocol(Protocol[T]):
    @property
    def logger(self) -> logging.Logger: ...

    @property
    def c(self) -> EasyvereinClient: ...

    @property
    def endpoint_name(self) -> str: ...

    @property
    def return_type(self) -> Type[T]: ...

    @property
    def scope_params(self) -> dict[str, Any]: ...
