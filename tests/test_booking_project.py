from easyverein import EasyvereinAPI
from easyverein.models import BookingProject, BookingProjectCreate, BookingProjectFilter, BookingProjectUpdate


class TestBookingProject:
    def test_get_booking_projects(self, ev_connection: EasyvereinAPI):
        """Test getting all booking projects"""
        booking_projects, total_count = ev_connection.booking_project.get()

        assert isinstance(booking_projects, list)
        assert isinstance(total_count, int)

        # Check if all booking projects are of type BookingProject
        for booking_project in booking_projects:
            assert isinstance(booking_project, BookingProject)

    def test_get_booking_project_by_id(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test getting a booking project by ID"""
        booking_project = ev_connection.booking_project.get_by_id(example_booking_project.id)

        assert isinstance(booking_project, BookingProject)
        assert booking_project.id == example_booking_project.id
        assert booking_project.name == example_booking_project.name

    def test_booking_project_create_and_delete(self, ev_connection: EasyvereinAPI, random_string: str):
        """Test creating and deleting a booking project"""
        # Create a new booking project with unique short code (max 4 chars)
        booking_project_data = {
            "name": f"Test Project {random_string}",
            "color": "#23985d",
            "short": random_string[:4],  # Use part of random string for unique short code (max 4 chars)
            "budget": "0.00",
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

        # Verify we can retrieve the created booking project by ID
        retrieved_project = ev_connection.booking_project.get_by_id(booking_project.id)
        assert isinstance(retrieved_project, BookingProject)
        assert retrieved_project.id == booking_project.id
        assert retrieved_project.name == booking_project.name

        # Clean up - delete the booking project
        ev_connection.booking_project.delete(booking_project)

    def test_booking_project_update(self, ev_connection: EasyvereinAPI, example_booking_project):
        """Test updating a booking project"""
        update_data = {
            "name": "Updated Project Name",
            "color": "#FF5733",
            "completed": True,
        }
        update_model = BookingProjectUpdate(**update_data)

        booking_project = ev_connection.booking_project.update(example_booking_project.id, update_model)

        assert isinstance(booking_project, BookingProject)
        assert booking_project.name == update_data["name"]
        assert booking_project.color == update_data["color"]
        assert booking_project.completed == update_data["completed"]

        # Reset the booking project back to original state for other tests
        reset_data = {
            "name": example_booking_project.name,  # Use the original name from the fixture
            "color": "#23985d",
            "completed": False,
        }
        reset_model = BookingProjectUpdate(**reset_data)
        ev_connection.booking_project.update(example_booking_project.id, reset_model)

    def test_booking_project_filter(self, ev_connection: EasyvereinAPI):
        """Test filtering booking projects"""
        # Get all booking projects first
        all_projects, _ = ev_connection.booking_project.get()

        if len(all_projects) > 0:
            # Use the name of the first project for filtering
            first_project = all_projects[0]
            filter_params = BookingProjectFilter(
                name=first_project.name,
            )

            booking_projects, _ = ev_connection.booking_project.get(search=filter_params)

            assert isinstance(booking_projects, list)
            # Should find at least the project we filtered by
            assert len(booking_projects) >= 1
            assert all(isinstance(bp, BookingProject) for bp in booking_projects)
        else:
            # If no projects exist, just test that filtering returns empty list
            filter_params = BookingProjectFilter(name="NonExistentProject")
            booking_projects, _ = ev_connection.booking_project.get(search=filter_params)

            assert isinstance(booking_projects, list)
            assert len(booking_projects) == 0
