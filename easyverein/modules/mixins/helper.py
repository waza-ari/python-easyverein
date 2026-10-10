from typing import Any, TypeVar, overload

from pydantic import BaseModel

from easyverein.core.exceptions import EasyvereinAPIException


def get_id(obj: BaseModel | int) -> int:
    if isinstance(obj, int):
        return obj

    if hasattr(obj, "id"):
        return obj.id  # type: ignore

    raise EasyvereinAPIException("Object does not have an id attribute")


T = TypeVar("T", bound=BaseModel)


@overload
def parse_models(result: dict[str, Any], return_model: type[T], context: dict[str, Any] | None = None) -> T: ...
@overload
def parse_models(
    result: list[dict[str, Any]], return_model: type[T], context: dict[str, Any] | None = None
) -> list[T]: ...
@overload
def parse_models(result: None, return_model: type[T], context: dict[str, Any] | None = None) -> None: ...
def parse_models(result, return_model: type[T], context: dict[str, Any] | None = None):
    """
    Validates API results into models. Pass the client context to translate field names of the
    configured API version.
    """
    if result is None:
        return None
    elif isinstance(result, list):
        return [return_model.model_validate(i, context=context) for i in result]
    elif isinstance(result, dict):
        return return_model.model_validate(result, context=context)
