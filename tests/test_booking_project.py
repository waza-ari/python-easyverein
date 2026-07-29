from typing import Generator

import pytest
from easyverein import EasyvereinAPI
from easyverein.models import BookingProject, BookingProjectCreate, BookingProjectFilter, BookingProjectUpdate


@pytest.fixture(scope="module", autouse=True)
def _remove_test_booking_projects(ev_connection: EasyvereinAPI) -> Generator[None, None, None]:
    yield
    for p in ev_connection.booking_project.get_all(query="{id,name}"):
        if p.name and p.name.lower().startswith("test_"):
            ev_connection.booking_project.delete(p, delete_from_recycle_bin=True)


class TestBookingProject:
    def test_get_booking_projects(self, ev_connection: EasyvereinAPI):
        booking_projects, total_count = ev_connection.booking_project.get(limit=50)
        assert isinstance(booking_projects, list)
        assert total_count >= len(booking_projects)
        for booking_project in booking_projects:
            assert isinstance(booking_project, BookingProject)

    def test_create_minimal_booking_project(self, ev_connection: EasyvereinAPI, random_string: str):
        booking_project = ev_connection.booking_project.create(
            BookingProjectCreate(name=f"test_{random_string}", short="TPM")
        )
        assert isinstance(booking_project, BookingProject)
        assert booking_project.name == f"test_{random_string}"
        assert isinstance(booking_project.id, int)

        ev_connection.booking_project.delete(booking_project)

        deleted_booking_projects, _ = ev_connection.booking_project.get_deleted()
        assert any(bp.id == booking_project.id for bp in deleted_booking_projects)

        ev_connection.booking_project.purge(booking_project.id)

        deleted_booking_projects, _ = ev_connection.booking_project.get_deleted()
        assert not any(bp.id == booking_project.id for bp in deleted_booking_projects)

    def test_create_and_update_booking_project(self, ev_connection: EasyvereinAPI, random_string: str):
        booking_project = ev_connection.booking_project.create(
            BookingProjectCreate(
                name=f"test_{random_string}_full",
                color="#112233",
                short="TP12",
                budget=1000.0,
                completed=False,
                projectCostCentre="KST-01",
            )
        )

        assert isinstance(booking_project, BookingProject)
        assert booking_project.name == f"test_{random_string}_full"
        assert booking_project.color == "#112233"
        assert booking_project.short == "TP12"
        assert booking_project.budget == 1000.0
        assert booking_project.completed is False
        assert booking_project.projectCostCentre == "KST-01"

        updated_booking_project = ev_connection.booking_project.update(
            booking_project.id,  # type: ignore[arg-type]
            BookingProjectUpdate(
                name=f"test_{random_string}_updated",
                budget=2000.0,
                completed=True,
            ),
        )

        assert isinstance(updated_booking_project, BookingProject)
        assert updated_booking_project.name == f"test_{random_string}_updated"
        assert updated_booking_project.budget == 2000.0
        assert updated_booking_project.completed is True
        assert updated_booking_project.color == "#112233"
        assert updated_booking_project.short == "TP12"
        assert updated_booking_project.projectCostCentre == "KST-01"

        ev_connection.booking_project.delete(booking_project, delete_from_recycle_bin=True)

    def test_filter_booking_projects(self, ev_connection: EasyvereinAPI, random_string: str):
        booking_project = ev_connection.booking_project.create(
            BookingProjectCreate(name=f"test_{random_string}_filter", short="TPF")
        )

        try:
            by_name = BookingProjectFilter(name=f"test_{random_string}_filter")
            booking_projects, total_count = ev_connection.booking_project.get(search=by_name)
            assert total_count >= 1
            assert any(bp.id == booking_project.id for bp in booking_projects)

            by_id = BookingProjectFilter(id__in=[booking_project.id])
            booking_projects, total_count = ev_connection.booking_project.get(search=by_id)
            assert total_count == 1
            assert booking_projects[0].id == booking_project.id
        finally:
            ev_connection.booking_project.delete(booking_project, delete_from_recycle_bin=True)
