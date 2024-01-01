import os
import random
import string

import pytest

from easyverein import EasyvereinAPI


@pytest.fixture
def ev_connection():
    api_url = os.getenv("EV_API_URL", "https://hexa.easyverein.com/api/")
    api_version = os.getenv("EV_API_VERSION", "v1.7")
    api_key = os.getenv("EV_API_KEY", "")

    return EasyvereinAPI(api_key, base_url=api_url, api_version=api_version)


@pytest.fixture(scope="function")
def random_string():
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )
