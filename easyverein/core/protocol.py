import logging
from typing import Protocol, TypeVar

from .client import EasyvereinClient


# noinspection PyPropertyDefinition
class IsEVClientProtocol(Protocol):
    @property
    def logger(self) -> logging.Logger:
        ...

    @property
    def c(self) -> EasyvereinClient:
        ...

    @property
    def endpoint_name(self) -> str:
        ...

    @property
    def model_class(self) -> TypeVar:
        ...
