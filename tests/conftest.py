import os

import pytest

from easyverein import EasyvereinAPI


@pytest.fixture
def ev_connection():
    api_url = os.getenv("EV_API_URL", "https://hexa.easyverein.com/api/")
    api_version = os.getenv("EV_API_VERSION", "v1.7")
    api_key = os.getenv("EV_API_KEY", "")

    return EasyvereinAPI(api_key, base_url=api_url, api_version=api_version)
