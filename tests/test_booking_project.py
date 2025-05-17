"""
Test BookingProject functionality
"""

import pytest
from easyverein.api import EasyvereinAPI
from easyverein.models import BookingProject, BookingProjectCreate


@pytest.fixture
def booking_project_data():
    """Create test data for booking project"""
    return {
        "name": "Test Project",
        "color": "#23985d",
        "short": "5001",
        "budget": "0.00",
        "completed": False,
        "projectCostCentre": "90001",
    }


@pytest.fixture
def booking_project_update_data():
    """Create test data for booking project update"""
    return {
        "name": "Updated Project",
        "color": "#FF5733",
        "completed": True,
    }


def test_booking_project_create(api_key, booking_project_data):
    """Test creating a booking project"""
    api = EasyvereinAPI(api_key)
    create_model = BookingProjectCreate(**booking_project_data)

    # Mocked in conftest.py
    booking_project = api.booking_project.create(create_model)

    assert isinstance(booking_project, BookingProject)
    assert booking_project.name == booking_project_data["name"]
    assert booking_project.color == booking_project_data["color"]
    assert booking_project.short == booking_project_data["short"]
    assert booking_project.budget == booking_project_data["budget"]
    assert booking_project.completed == booking_project_data["completed"]
    assert booking_project.projectCostCentre == booking_project_data["projectCostCentre"]


def test_booking_project_get(api_key):
    """Test getting a booking project"""
    api = EasyvereinAPI(api_key)

    # Mocked in conftest.py
    booking_project = api.booking_project.get(123)

    assert isinstance(booking_project, BookingProject)
    assert booking_project.id == 123


def test_booking_project_update(api_key, booking_project_update_data):
    """Test updating a booking project"""
    api = EasyvereinAPI(api_key)

    # Mocked in conftest.py
    booking_project = api.booking_project.update(123, booking_project_update_data)

    assert isinstance(booking_project, BookingProject)
    assert booking_project.name == booking_project_update_data["name"]
    assert booking_project.color == booking_project_update_data["color"]
    assert booking_project.completed == booking_project_update_data["completed"]


def test_booking_project_filter(api_key):
    """Test filtering booking projects"""
    api = EasyvereinAPI(api_key)
    filter_params = {
        "name": "Test",
        "completed": False,
    }

    # Mocked in conftest.py
    booking_projects = api.booking_project.filter(filter_params)

    assert isinstance(booking_projects, list)
    assert len(booking_projects) > 0
    assert all(isinstance(bp, BookingProject) for bp in booking_projects)


def test_booking_project_delete(api_key):
    """Test deleting a booking project"""
    api = EasyvereinAPI(api_key)

    # Mocked in conftest.py
    result = api.booking_project.delete(123)

    assert result is True
