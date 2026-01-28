import os
import random
import string

import pytest
from easyverein import EasyvereinAPI
from easyverein.models import BookingProjectCreate, CustomFieldCreate


@pytest.fixture(scope="session")
def ev_connection():
    api_url = os.getenv("EV_API_URL", "https://easyverein.com/api/")
    api_version = os.getenv("EV_API_VERSION", "v2.0")
    api_key = os.getenv("EV_API_KEY", "")

    return EasyvereinAPI(api_key, base_url=api_url, api_version=api_version, auto_retry=True)


@pytest.fixture(scope="module", autouse=True)
def _clear_wastebaskets(ev_connection: EasyvereinAPI):
    for module in ["member_group", "custom_field", "contact_details", "billing_account"]:
        deleted, _ = getattr(ev_connection, module).get_deleted()
        for d in deleted:
            getattr(ev_connection, module).purge(d)


@pytest.fixture(scope="function")
def random_string():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


@pytest.fixture(scope="module")
def example_member(ev_connection):
    members, _ = ev_connection.member.get()
    return members[0]


@pytest.fixture(scope="module")
def example_custom_field(ev_connection):
    custom_field = ev_connection.custom_field.create(CustomFieldCreate(name="Test-Field", kind="e", settings_type="t"))
    yield custom_field
    ev_connection.custom_field.delete(custom_field)
    ev_connection.custom_field.purge(custom_field.id)


@pytest.fixture(scope="module")
def example_booking_project(ev_connection):
    # Generate unique identifiers using timestamp to avoid collisions
    import time

    timestamp = str(int(time.time()))
    unique_short = timestamp[-4:]  # Use last 4 digits of timestamp
    unique_name = f"Test-Project-{timestamp[-6:]}"  # Use last 6 digits for name
    booking_project = ev_connection.booking_project.create(
        BookingProjectCreate(
            name=unique_name,
            color="#23985d",
            short=unique_short,
            budget="0.00",
            completed=False,
            projectCostCentre="90001",
        )
    )
    yield booking_project
    ev_connection.booking_project.delete(booking_project)


@pytest.fixture(scope="function")
def api_key():
    return "test_api_key"
