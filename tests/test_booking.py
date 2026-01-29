import datetime
from typing import Generator

import pytest
from easyverein import EasyvereinAPI
from easyverein.models import Booking, BookingCreate, BookingUpdate


@pytest.fixture(scope="module", autouse=True)
def _remove_test_bookings(ev_connection: EasyvereinAPI) -> Generator[None, None, None]:
    yield
    for b in ev_connection.booking.get_all(query="{id,receiver}"):
        if b.receiver and b.receiver.lower().startswith("test_"):
            ev_connection.booking.delete(b, delete_from_recycle_bin=True)


class TestBooking:
    def test_get_bookings(self, ev_connection: EasyvereinAPI):
        bookings, total_count = ev_connection.booking.get()
        assert isinstance(bookings, list)

    def test_create_booking_minimal(self, ev_connection: EasyvereinAPI, random_string: str):
        booking_model = BookingCreate(
            receiver=f"test_{random_string}",
            date=datetime.date.today(),
            amount=100.0,
        )

        booking = ev_connection.booking.create(booking_model)
        assert isinstance(booking, Booking)
        assert booking.receiver == booking_model.receiver

        ev_connection.booking.delete(booking, delete_from_recycle_bin=True)


class TestBookingBulk:
    def test_bulk_create(self, ev_connection: EasyvereinAPI, random_string: str):
        name = random_string
        booking_data = [
            BookingCreate(
                receiver=f"test_{name}1",
                date=datetime.date.today(),
                amount=100.0,
            ),
            BookingCreate(
                receiver=f"test_{name}2",
                date=datetime.date.today(),
                amount=200.0,
            ),
        ]

        successes = ev_connection.booking.bulk_create(booking_data)
        assert successes == [True, True]

        created_bookings = [
            b
            for b in ev_connection.booking.get_all(query="{id,receiver}")
            if b.receiver and b.receiver.startswith(f"test_{name}")
        ]

        assert len(created_bookings) == 2

    def test_bulk_update(self, ev_connection: EasyvereinAPI, random_string: str):
        # Create two bookings
        name = random_string
        b1 = ev_connection.booking.create(
            BookingCreate(
                receiver=f"test_{name}3",
                date=datetime.date.today(),
                amount=300.0,
            )
        )
        b2 = ev_connection.booking.create(
            BookingCreate(
                receiver=f"test_{name}4",
                date=datetime.date.today(),
                amount=400.0,
            )
        )

        update_data = [
            BookingUpdate(id=b1.id, description="Updated Description 1"),
            BookingUpdate(id=b2.id, description="Updated Description 2"),
        ]

        successes = ev_connection.booking.bulk_update(update_data)
        assert successes == [True, True]

        updated_b1 = ev_connection.booking.get_by_id(b1.id)  # type: ignore
        updated_b2 = ev_connection.booking.get_by_id(b2.id)  # type: ignore

        assert updated_b1.description == "Updated Description 1"
        assert updated_b2.description == "Updated Description 2"
