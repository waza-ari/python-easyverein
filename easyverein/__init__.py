"""
Middleware for FastAPI that supports authenticating users against Keycloak
"""

__version__ = "1.1.2"

# Export EasyVerein API directly
from .api import EasyvereinAPI  # noqa: F401
from .core.exceptions import (  # noqa: F401
    EasyvereinAPIException,
    EasyvereinAPINotFoundException,
    EasyvereinAPITooManyRetriesException,
)
from .core.responses import BearerToken
