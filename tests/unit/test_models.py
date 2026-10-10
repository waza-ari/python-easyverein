"""Unit tests for Pydantic model validation (no API connection required)."""

import pytest
from easyverein.models import BillingAccount, Booking, InvoiceItem
from easyverein.models.member_group import MemberGroup
from pydantic import ValidationError


class TestMemberGroupModel:
    """Unit tests for MemberGroup model validation."""

    def test_payment_interval_negative_one(self):
        """Test that paymentInterval accepts -1 for one-time payments."""
        # The EasyVerein API returns -1 for groups with one-time payments (e.g., registration fees)
        member_group = MemberGroup(paymentInterval=-1)
        assert member_group.paymentInterval == -1

    def test_payment_interval_positive(self):
        """Test that paymentInterval accepts positive integers."""
        member_group = MemberGroup(paymentInterval=12)
        assert member_group.paymentInterval == 12

    def test_payment_interval_none(self):
        """Test that paymentInterval accepts None."""
        member_group = MemberGroup(paymentInterval=None)
        assert member_group.paymentInterval is None

    def test_payment_interval_invalid_negative(self):
        """Test that paymentInterval rejects invalid negative values (other than -1)."""
        with pytest.raises(ValidationError):
            MemberGroup(paymentInterval=-2)

    def test_payment_interval_zero_invalid(self):
        """Test that paymentInterval rejects zero."""
        with pytest.raises(ValidationError):
            MemberGroup(paymentInterval=0)


class TestSphere:
    """Unit tests for the SKR 42 sphere values."""

    @pytest.mark.parametrize("sphere", [1, 4, 9, 11, 31, 49])
    def test_valid_spheres(self, sphere: int):
        """Test that main spheres, Sammelposten and sub-spheres are accepted."""
        assert BillingAccount(defaultSphere=sphere).defaultSphere == sphere
        assert Booking(sphere=sphere).sphere == sphere
        assert InvoiceItem(sphere=sphere).sphere == sphere
        assert MemberGroup(sphere=sphere).sphere == sphere

    @pytest.mark.parametrize("sphere", [0, 5, 10, 20, 50])
    def test_invalid_spheres(self, sphere: int):
        """Test that values unknown to the API are rejected."""
        with pytest.raises(ValidationError):
            Booking(sphere=sphere)
