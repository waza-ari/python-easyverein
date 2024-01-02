import os
import random
import string

import pytest

from easyverein import EasyvereinAPI
from easyverein.models import CustomFieldCreate


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="module")
def example_member(ev_connection):
    return ev_connection.member.get()[1]


@pytest.fixture(scope="module")
def example_custom_field(ev_connection):
    custom_field = ev_connection.custom_field.create(
        CustomFieldCreate(name="Test-Field", kind="e", settings_type="t")
    )
    yield custom_field
    ev_connection.custom_field.delete(custom_field)
