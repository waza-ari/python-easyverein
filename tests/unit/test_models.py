"""Unit tests for Pydantic model validation (no API connection required)."""

import pytest
from pydantic import ValidationError

from easyverein.models.member_group import MemberGroup


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
