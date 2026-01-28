import pytest
from easyverein import EasyvereinAPI
from easyverein.models import BookingProject, BookingProjectCreate, BookingProjectFilter, BookingProjectUpdate


class TestBookingProject:
    """Test suite for BookingProject API operations"""

    def test_get_booking_projects(self, ev_connection: EasyvereinAPI):
        """Test fetching all booking projects returns correct types"""
        booking_projects, total_count = ev_connection.booking_project.get()

        assert isinstance(booking_projects, list)
        assert isinstance(total_count, int)
        assert total_count >= 0

        for booking_project in booking_projects:
            assert isinstance(booking_project, BookingProject)

    def test_get_booking_projects_with_limit(self, ev_connection: EasyvereinAPI):
        """Test fetching booking projects with a limit parameter"""
        booking_projects, total_count = ev_connection.booking_project.get(limit=5)

        assert isinstance(booking_projects, list)
        assert len(booking_projects) <= 5

        for booking_project in booking_projects:
            assert isinstance(booking_project, BookingProject)

    def test_get_all_booking_projects(self, ev_connection: EasyvereinAPI):
        """Test fetching all booking projects with pagination abstracted"""
        booking_projects = ev_connection.booking_project.get_all(limit_per_page=10)

        assert isinstance(booking_projects, list)

        for booking_project in booking_projects:
            assert isinstance(booking_project, BookingProject)

    def test_get_booking_project_by_id(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test retrieving a specific booking project by ID"""
        booking_project = ev_connection.booking_project.get_by_id(example_booking_project.id)

        assert isinstance(booking_project, BookingProject)
        assert booking_project.id == example_booking_project.id
        assert booking_project.name == example_booking_project.name
        assert booking_project.short == example_booking_project.short

    def test_create_booking_project_minimal(self, ev_connection: EasyvereinAPI, random_string: str):
        """Test creating a booking project with only required fields"""
        create_model = BookingProjectCreate(name=f"Minimal Project {random_string}")

        booking_project = ev_connection.booking_project.create(create_model)

        assert isinstance(booking_project, BookingProject)
        assert isinstance(booking_project.id, int)
        assert booking_project.name == create_model.name

        # Clean up
        ev_connection.booking_project.delete(booking_project)

    def test_create_booking_project_with_all_fields(self, ev_connection: EasyvereinAPI, random_string: str):
        """Test creating a booking project with all available fields"""
        booking_project_data = {
            "name": f"Full Project {random_string}",
            "color": "#23985d",
            "short": random_string[:4],  # Max 4 characters
            "budget": "1500.00",
            "completed": False,
            "projectCostCentre": "90001",
        }

        create_model = BookingProjectCreate(**booking_project_data)
        booking_project = ev_connection.booking_project.create(create_model)

        assert isinstance(booking_project, BookingProject)
        assert booking_project.name == booking_project_data["name"]
        assert booking_project.color == booking_project_data["color"]
        assert booking_project.short == booking_project_data["short"]
        assert booking_project.budget == booking_project_data["budget"]
        assert booking_project.completed == booking_project_data["completed"]
        assert booking_project.projectCostCentre == booking_project_data["projectCostCentre"]
        assert isinstance(booking_project.id, int)

        # Verify retrieval matches creation
        retrieved_project = ev_connection.booking_project.get_by_id(booking_project.id)
        assert retrieved_project.id == booking_project.id
        assert retrieved_project.name == booking_project.name

        # Clean up
        ev_connection.booking_project.delete(booking_project)

    def test_update_booking_project(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test updating a booking project's fields"""
        original_name = example_booking_project.name
        original_color = example_booking_project.color
        original_completed = example_booking_project.completed

        update_data = BookingProjectUpdate(
            name="Updated Project Name",
            color="#FF5733",
            completed=True,
        )

        updated_project = ev_connection.booking_project.update(example_booking_project.id, update_data)

        assert isinstance(updated_project, BookingProject)
        assert updated_project.id == example_booking_project.id
        assert updated_project.name == "Updated Project Name"
        assert updated_project.color == "#FF5733"
        assert updated_project.completed is True

        # Reset to original state for other tests
        reset_model = BookingProjectUpdate(
            name=original_name,
            color=original_color or "#23985d",
            completed=original_completed or False,
        )
        ev_connection.booking_project.update(example_booking_project.id, reset_model)

    def test_update_booking_project_partial(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test partial update of a booking project (only some fields)"""
        original_budget = example_booking_project.budget

        # Only update budget
        update_data = BookingProjectUpdate(budget="2500.00")
        updated_project = ev_connection.booking_project.update(example_booking_project.id, update_data)

        assert isinstance(updated_project, BookingProject)
        assert updated_project.budget == "2500.00"
        # Other fields should remain unchanged
        assert updated_project.name == example_booking_project.name

        # Reset budget
        reset_model = BookingProjectUpdate(budget=original_budget or "0.00")
        ev_connection.booking_project.update(example_booking_project.id, reset_model)

    def test_filter_booking_projects_by_name(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test filtering booking projects by name"""
        filter_params = BookingProjectFilter(name=example_booking_project.name)
        booking_projects, _ = ev_connection.booking_project.get(search=filter_params)

        assert isinstance(booking_projects, list)
        assert len(booking_projects) >= 1
        assert all(isinstance(bp, BookingProject) for bp in booking_projects)
        # The fixture project should be in results
        project_names = [bp.name for bp in booking_projects]
        assert example_booking_project.name in project_names

    def test_filter_booking_projects_by_short(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test filtering booking projects by short code"""
        filter_params = BookingProjectFilter(short=example_booking_project.short)
        booking_projects, _ = ev_connection.booking_project.get(search=filter_params)

        assert isinstance(booking_projects, list)
        assert len(booking_projects) >= 1
        # All results should have matching short code
        for bp in booking_projects:
            assert bp.short == example_booking_project.short

    def test_filter_booking_projects_by_completed(self, ev_connection: EasyvereinAPI):
        """Test filtering booking projects by completion status"""
        filter_params = BookingProjectFilter(completed=False)
        booking_projects, _ = ev_connection.booking_project.get(search=filter_params)

        assert isinstance(booking_projects, list)
        for bp in booking_projects:
            assert isinstance(bp, BookingProject)
            assert bp.completed is False

    def test_filter_booking_projects_nonexistent(self, ev_connection: EasyvereinAPI):
        """Test filtering with criteria that match no projects"""
        filter_params = BookingProjectFilter(name="NonExistentProjectXYZ123456789")
        booking_projects, total_count = ev_connection.booking_project.get(search=filter_params)

        assert isinstance(booking_projects, list)
        assert len(booking_projects) == 0

    def test_delete_booking_project(self, ev_connection: EasyvereinAPI, random_string: str):
        """Test deleting a booking project"""
        # Create a project to delete
        create_model = BookingProjectCreate(
            name=f"To Delete {random_string}",
            short=random_string[:4],
        )
        booking_project = ev_connection.booking_project.create(create_model)
        project_id = booking_project.id

        # Verify it exists
        retrieved = ev_connection.booking_project.get_by_id(project_id)
        assert retrieved.id == project_id

        # Delete it
        ev_connection.booking_project.delete(booking_project)

        # Verify it's gone (should raise an exception when trying to fetch)
        from easyverein.core.exceptions import EasyvereinAPIException

        with pytest.raises(EasyvereinAPIException):
            ev_connection.booking_project.get_by_id(project_id)

    def test_booking_project_model_attributes(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test that booking project model has expected attributes"""
        booking_project = ev_connection.booking_project.get_by_id(example_booking_project.id)

        # Verify all expected attributes exist
        assert hasattr(booking_project, "id")
        assert hasattr(booking_project, "name")
        assert hasattr(booking_project, "color")
        assert hasattr(booking_project, "short")
        assert hasattr(booking_project, "budget")
        assert hasattr(booking_project, "completed")
        assert hasattr(booking_project, "projectCostCentre")

        # Verify types where applicable
        assert isinstance(booking_project.id, int)
        assert isinstance(booking_project.name, str)
