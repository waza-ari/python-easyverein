from easyverein import EasyvereinAPI
from easyverein.models.billing_account import (
    BillingAccount,
    BillingAccountCreate,
    BillingAccountFilter,
    BillingAccountUpdate,
)


class TestBillingAccount:
    def test_get_billing_accounts(self, ev_connection: EasyvereinAPI):
        limit = 50
        billing_accounts, total_count = ev_connection.billing_account.get(limit=limit)
        # Check if the response is a list
        assert isinstance(billing_accounts, list)

        # Check if all the billing accounts are of type BillingAccount
        for billing_account in billing_accounts:
            assert isinstance(billing_account, BillingAccount)

        # Verify total_count matches the length
        assert len(billing_accounts) == limit

    def test_create_minimal_billing_account(self, ev_connection: EasyvereinAPI):
        # Get current count
        _, old_total_count = ev_connection.billing_account.get()

        billing_account = ev_connection.billing_account.create(BillingAccountCreate(name="Test Account", number=9999))
        assert isinstance(billing_account, BillingAccount)
        assert billing_account.name == "Test Account"
        assert billing_account.number == 9999
        assert billing_account.numberLength == 4
        assert billing_account.linkedBookings == 0
        assert billing_account.accountingPlans == []
        assert isinstance(billing_account.id, int)

        # Verify we have one more billing account
        billing_accounts, total_count = ev_connection.billing_account.get()
        assert total_count == old_total_count + 1

        # Delete the billing account again, should only soft delete them
        ev_connection.billing_account.delete(billing_account)

        # Get entries from wastebasket
        deleted_billing_accounts, _ = ev_connection.billing_account.get_deleted()
        assert len(deleted_billing_accounts) == 1
        assert deleted_billing_accounts[0].id == billing_account.id

        # Finally purge billing account from wastebasket
        ev_connection.billing_account.purge(billing_account.id)

        # Get entries from wastebasket
        deleted_billing_accounts, _ = ev_connection.billing_account.get_deleted()
        assert len(deleted_billing_accounts) == 0

        # Verify count is back to original
        billing_accounts, total_count = ev_connection.billing_account.get()
        assert total_count == old_total_count

    def test_create_billing_account_with_all_fields(self, ev_connection: EasyvereinAPI):
        billing_account = ev_connection.billing_account.create(
            BillingAccountCreate(
                name="Full Test Account",
                number=8888,
                excludeInEur=True,
                defaultSphere=1,
            )
        )

        assert isinstance(billing_account, BillingAccount)
        assert billing_account.name == "Full Test Account"
        assert billing_account.number == 8888
        assert billing_account.excludeInEur is True
        assert billing_account.defaultSphere == 1
        assert billing_account.numberLength == 4
        assert billing_account.linkedBookings == 0
        assert billing_account.accountingPlans == []
        assert isinstance(billing_account.id, int)

        # Modify the billing account
        updated_account = ev_connection.billing_account.update(
            billing_account.id,
            BillingAccountUpdate(name="Updated Account Name", excludeInEur=False),
        )

        assert isinstance(updated_account, BillingAccount)
        assert updated_account.name == "Updated Account Name"
        assert updated_account.excludeInEur is False
        # Number should remain unchanged
        assert updated_account.number == 8888

        # Delete the billing account again
        ev_connection.billing_account.delete(billing_account, delete_from_recycle_bin=True)

    def test_update_billing_account(self, ev_connection: EasyvereinAPI):
        # Create a billing account
        billing_account = ev_connection.billing_account.create(
            BillingAccountCreate(name="Update Test Account", number=7777)
        )

        assert isinstance(billing_account, BillingAccount)
        assert billing_account.name == "Update Test Account"
        assert billing_account.number == 7777
        assert isinstance(billing_account.id, int)

        # Update only the name
        updated_account = ev_connection.billing_account.update(
            billing_account.id, BillingAccountUpdate(name="Updated Name")
        )

        assert isinstance(updated_account, BillingAccount)
        assert updated_account.name == "Updated Name"
        assert updated_account.number == 7777  # Should remain unchanged

        # Update only the number
        updated_account = ev_connection.billing_account.update(billing_account.id, BillingAccountUpdate(number=6666))

        assert isinstance(updated_account, BillingAccount)
        assert updated_account.name == "Updated Name"  # Should remain unchanged
        assert updated_account.number == 6666

        # Clean up
        ev_connection.billing_account.delete(billing_account, delete_from_recycle_bin=True)

    def test_filter_billing_accounts(self, ev_connection: EasyvereinAPI):
        # Create a test billing account for filtering
        test_account = ev_connection.billing_account.create(
            BillingAccountCreate(name="Filter Test Account", number=5555, skr="42")
        )
        assert isinstance(test_account.id, int)

        try:
            # Test filter by name
            search = BillingAccountFilter(name="Filter Test Account")
            billing_accounts, total_count = ev_connection.billing_account.get(search=search)
            assert len(billing_accounts) >= 1
            assert any(ba.name == "Filter Test Account" for ba in billing_accounts)

            # Test filter by skr
            search = BillingAccountFilter(skr="42")
            billing_accounts, total_count = ev_connection.billing_account.get(search=search)
            assert len(billing_accounts) >= 1
            assert any(ba.skr == "42" for ba in billing_accounts)

            # Test filter by number range
            search = BillingAccountFilter(number__gte=5550, number__lte=5560)
            billing_accounts, total_count = ev_connection.billing_account.get(search=search)
            assert len(billing_accounts) >= 1
            assert any(ba.number == 5555 for ba in billing_accounts)

            # Test filter by id
            search = BillingAccountFilter(id__in=[test_account.id])
            billing_accounts, total_count = ev_connection.billing_account.get(search=search)
            assert len(billing_accounts) == 1
            assert billing_accounts[0].id == test_account.id

        finally:
            # Clean up
            ev_connection.billing_account.delete(test_account, delete_from_recycle_bin=True)

    def test_get_billing_account_by_id(self, ev_connection: EasyvereinAPI):
        # Create a billing account
        billing_account = ev_connection.billing_account.create(BillingAccountCreate(name="Get By ID Test", number=4444))
        assert isinstance(billing_account.id, int)

        try:
            # Get by ID
            retrieved_account = ev_connection.billing_account.get_by_id(billing_account.id)

            assert isinstance(retrieved_account, BillingAccount)
            assert retrieved_account.id == billing_account.id
            assert retrieved_account.name == "Get By ID Test"
            assert retrieved_account.number == 4444
        finally:
            # Clean up
            ev_connection.billing_account.delete(billing_account, delete_from_recycle_bin=True)
