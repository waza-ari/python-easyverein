"""
This module contains the base class translating field names between the supported API versions.
"""

from typing import Any, ClassVar

from pydantic import (
    BaseModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    ValidationInfo,
    model_serializer,
    model_validator,
)

from ...core.api_version import API_V3, API_VERSION_CONTEXT_KEY, to_snake_case

# Per class cache: (v2 serialization key -> v3 name, v3 name -> validation key)
_NAME_MAPS: dict[type, tuple[dict[str, str | None], dict[str, str]]] = {}


class VersionedModel(BaseModel):
    """
    Base class for all models exchanged with the API.

    The attribute names of the models follow the naming of API v2.0. When a model is validated or serialized with
    a context `{"api_version": "v3.0"}` (which the client does automatically), field names are translated to and
    from the snake_case names used by API v3.0.

    By default, the v3.0 name is derived from the v2.0 name using
    [`to_snake_case`][easyverein.core.api_version.to_snake_case]. Subclasses can override this in
    `__v3_names__`, mapping the Python attribute name to the v3.0 name. Mapping to `None` marks a field
    as not supported by API v3.0, serializing it then raises an error.
    """

    __v3_names__: ClassVar[dict[str, str | None]] = {}

    @classmethod
    def _name_maps(cls) -> tuple[dict[str, str | None], dict[str, str]]:
        if cls not in _NAME_MAPS:
            overrides: dict[str, str | None] = {}
            for klass in reversed(cls.__mro__):
                overrides.update(klass.__dict__.get("__v3_names__", {}))
            to_v3: dict[str, str | None] = {}
            from_v3: dict[str, str] = {}
            for name, field in cls.model_fields.items():
                serialization_key = field.serialization_alias or field.alias or name
                validation_key = field.validation_alias if isinstance(field.validation_alias, str) else None
                validation_key = validation_key or field.alias or name
                v3_name = overrides[name] if name in overrides else to_snake_case(serialization_key)
                to_v3[serialization_key] = v3_name
                if v3_name is not None:
                    from_v3[v3_name] = validation_key
            _NAME_MAPS[cls] = (to_v3, from_v3)
        return _NAME_MAPS[cls]

    @classmethod
    def wire_name(cls, field_name: str, api_version: str) -> str | None:
        """
        Returns the name the given API version uses for the given attribute, `None` if not supported.
        """
        field = cls.model_fields[field_name]
        v2_name = field.serialization_alias or field.alias or field_name
        return cls._name_maps()[0][v2_name] if api_version == API_V3 else v2_name

    @model_validator(mode="before")
    @classmethod
    def _rename_from_v3(cls, data: Any, info: ValidationInfo) -> Any:
        if (info.context or {}).get(API_VERSION_CONTEXT_KEY) != API_V3 or not isinstance(data, dict):
            return data
        from_v3 = cls._name_maps()[1]
        return {from_v3.get(key, key): value for key, value in data.items()}

    @model_serializer(mode="wrap")
    def _rename_to_v3(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> Any:
        data = handler(self)
        context = info.context or {}
        if context.get(API_VERSION_CONTEXT_KEY) != API_V3 or not info.by_alias or not isinstance(data, dict):
            return data
        to_v3 = self._name_maps()[0]
        renamed = {}
        for key, value in data.items():
            v3_key = to_v3.get(key, key)
            if v3_key is None:
                raise ValueError(f"{type(self).__name__}.{key} is not supported by API v3.0")
            renamed[v3_key] = value
        return renamed
