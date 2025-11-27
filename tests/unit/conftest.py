"""Conftest for unit tests - no API connection required."""

import pytest


@pytest.fixture(scope="module", autouse=True)
def _clear_wastebaskets():
    """Override parent conftest fixture - no-op for unit tests."""
    pass
