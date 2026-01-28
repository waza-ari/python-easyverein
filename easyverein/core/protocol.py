import logging
from typing import Protocol, Type, TypeVar

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
