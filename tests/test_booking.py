import datetime

from easyverein import EasyvereinAPI
from easyverein.models.booking import Booking, BookingCreate, BookingFilter, BookingUpdate


class TestBookings:
    def test_get_bookings(self, ev_connection: EasyvereinAPI):
        bookings, total_count = ev_connection.booking.get()
        # Check if the response is a list
        assert isinstance(bookings, list)

        # Check if all the bookings are of type Booking
        for booking in bookings:
            assert isinstance(booking, Booking)

    def test_get_bookings_with_filter(self, ev_connection: EasyvereinAPI):
        # Test filtering by blocked status
        filter_obj = BookingFilter(blocked=False)
        bookings, total_count = ev_connection.booking.get(filter=filter_obj)

        assert isinstance(bookings, list)
        for booking in bookings:
            assert isinstance(booking, Booking)
            if booking.blocked is not None:
                assert booking.blocked is False

    def test_get_bookings_with_invoice_filter(self, ev_connection: EasyvereinAPI):
        # Test filtering bookings that have related invoices
        filter_obj = BookingFilter(relatedInvoice__isnull=False)
        bookings, total_count = ev_connection.booking.get(filter=filter_obj)

        assert isinstance(bookings, list)
        for booking in bookings:
            assert isinstance(booking, Booking)

    def test_create_booking_minimal(self, ev_connection: EasyvereinAPI, random_string: str):
        # Create a minimal booking
        booking_model = BookingCreate(
            receiver=f"Test Receiver {random_string}",
            date=datetime.datetime.now(),
            amount=100.50,
            description="Test booking for API",
        )

        booking = ev_connection.booking.create(booking_model)

        # Check if the response is a Booking
        assert isinstance(booking, Booking)
        assert isinstance(booking.id, int)
        assert booking.receiver == booking_model.receiver

        # Clean up: delete booking
        ev_connection.booking.delete(booking, delete_from_recycle_bin=True)

    def test_create_booking_with_project(
        self, ev_connection: EasyvereinAPI, random_string: str, example_booking_project
    ):
        # Create a booking with a booking project reference
        booking_model = BookingCreate(
            receiver=f"Test Receiver {random_string}",
            date=datetime.datetime.now(),
            amount=250.75,
            description="Test booking with project",
            bookingProject=example_booking_project.id,
        )

        booking = ev_connection.booking.create(booking_model)

        # Check if the response is a Booking
        assert isinstance(booking, Booking)
        assert isinstance(booking.id, int)
        assert booking.bookingProject is not None

        # Clean up: delete booking
        ev_connection.booking.delete(booking, delete_from_recycle_bin=True)

    def test_update_booking(self, ev_connection: EasyvereinAPI, random_string: str):
        # Create a booking first
        booking_model = BookingCreate(
            receiver=f"Initial Receiver {random_string}",
            date=datetime.datetime.now(),
            amount=50.00,
        )

        booking = ev_connection.booking.create(booking_model)
        assert isinstance(booking, Booking)
        assert booking.id is not None

        # Update the booking
        new_description = f"Updated description {random_string}"
        updated_booking = ev_connection.booking.update(
            booking.id,
            BookingUpdate(description=new_description, amount=75.50),
        )

        assert isinstance(updated_booking, Booking)
        assert updated_booking.id == booking.id
        assert updated_booking.description == new_description
        assert updated_booking.amount == 75.50

        # Clean up: delete booking
        ev_connection.booking.delete(booking, delete_from_recycle_bin=True)

    def test_booking_with_invoice_relation(self, ev_connection: EasyvereinAPI, random_string: str, example_member):
        # First, get existing invoices to potentially link
        invoices, _ = ev_connection.booking.c.api_instance.invoice.get(limit=1)

        if len(invoices) > 0:
            invoice = invoices[0]

            # Test that we can query bookings with specific invoice relation
            filter_obj = BookingFilter(relatedInvoice=invoice.id)
            bookings, _ = ev_connection.booking.get(filter=filter_obj)

            assert isinstance(bookings, list)
            for booking in bookings:
                assert isinstance(booking, Booking)

    def test_booking_recycle_bin(self, ev_connection: EasyvereinAPI, random_string: str):
        # Create a booking
        booking_model = BookingCreate(
            receiver=f"Test Receiver {random_string}",
            date=datetime.datetime.now(),
            amount=100.00,
        )

        booking = ev_connection.booking.create(booking_model)
        assert isinstance(booking, Booking)
        assert booking.id is not None

        # Delete booking - should now be in recycle bin
        ev_connection.booking.delete(booking)

        # Get entries from wastebasket
        deleted_bookings, _ = ev_connection.booking.get_deleted()
        deleted_ids = [b.id for b in deleted_bookings]
        assert booking.id in deleted_ids

        # Finally purge booking from wastebasket
        ev_connection.booking.purge(booking.id)

        # Verify it's gone from recycle bin
        deleted_bookings_after, _ = ev_connection.booking.get_deleted()
        deleted_ids_after = [b.id for b in deleted_bookings_after]
        assert booking.id not in deleted_ids_after

    def test_booking_filter_by_date_range(self, ev_connection: EasyvereinAPI):
        # Test filtering bookings by date range
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=365)

        filter_obj = BookingFilter(
            date__gt=start_date,
            date__lt=end_date,
        )

        bookings, total_count = ev_connection.booking.get(filter=filter_obj)

        assert isinstance(bookings, list)
        for booking in bookings:
            assert isinstance(booking, Booking)
            if booking.date:
                # Verify dates are within range
                assert booking.date >= start_date
                assert booking.date <= end_date

    def test_booking_filter_by_amount(self, ev_connection: EasyvereinAPI):
        # Test filtering bookings by amount
        filter_obj = BookingFilter(
            amount=100.0,
        )

        bookings, total_count = ev_connection.booking.get(filter=filter_obj)

        assert isinstance(bookings, list)
        for booking in bookings:
            assert isinstance(booking, Booking)

    def test_booking_payment_difference_filter(self, ev_connection: EasyvereinAPI):
        # Test filtering by payment difference
        filter_obj = BookingFilter(
            paymentDifference__ne=0.0,
        )

        bookings, total_count = ev_connection.booking.get(filter=filter_obj)

        assert isinstance(bookings, list)
        for booking in bookings:
            assert isinstance(booking, Booking)
