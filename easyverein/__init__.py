"""
Middleware for FastAPI that supports authenticating users against Keycloak
"""

__version__ = "0.0.1"

# Export EasyVerein API directly
from .api import EasyvereinAPI  # noqa: F401
