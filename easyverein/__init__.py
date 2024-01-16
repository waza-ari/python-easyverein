"""
Middleware for FastAPI that supports authenticating users against Keycloak
"""

__version__ = "0.2.3"

# Export EasyVerein API directly
from .api import EasyvereinAPI  # noqa: F401
from .core.exceptions import (  # noqa: F401
    EasyvereinAPIException,
    EasyvereinAPINotFoundException,
    EasyvereinAPITooManyRetriesException,
)
