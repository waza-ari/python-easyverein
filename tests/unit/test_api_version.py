"""Unit tests for the translation between API v2.0 and v3.0 naming (no API connection required)."""

import datetime

import pytest
from easyverein import EasyvereinAPI
from easyverein.core.api_version import to_snake_case, translate_query
from easyverein.models import (
    BookingFilter,
    ContactDetails,
    ContactDetailsCreate,
    ContactDetailsFilter,
    CustomField,
    InvoiceCreate,
    InvoiceFilter,
    InvoiceItemFilter,
    Member,
    MemberFilter,
    MemberSetLsb,
)
from pydantic_core import PydanticSerializationError

V2 = {"api_version": "v2.0"}
V3 = {"api_version": "v3.0"}


@pytest.mark.parametrize(
    "v2_name, v3_name",
    [
        ("firstName", "first_name"),
        ("_isCompany", "is_company"),
        ("_deleteAfterDate", "delete_after_date"),
        ("user_allowICSExport", "user_allow_ics_export"),
        ("showEPCQRCode", "show_epcqr_code"),
        ("membershipCTEDownload", "membership_cte_download"),
        ("availableSkr42Spheres", "available_skr42_spheres"),
        ("settings_type", "settings_type"),
        ("contactDetails__preferredCommunicationWay__ne", "contact_details__preferred_communication_way__ne"),
        ("_applicationDate__isnull", "application_date__isnull"),
    ],
)
def test_to_snake_case(v2_name: str, v3_name: str):
    assert to_snake_case(v2_name) == v3_name


def test_translate_query():
    query = "{id,contactDetails{firstName,_isCompany,geoPositionCoords},memberGroups{memberGroup{short}},-org}"
    assert translate_query(query, "v3.0") == (
        "{id,contact_details{first_name,is_company,geo_position_coordinates},member_groups{member_group{short}},-org}"
    )
    # Already translated queries and v2.0 queries are left untouched
    assert translate_query("{id,first_name}", "v3.0") == "{id,first_name}"
    assert translate_query(query, "v2.0") == query


class TestModelTranslation:
    def test_parse_v3_response(self):
        member = Member.model_validate(
            {
                "id": 1,
                "delete_after_date": None,
                "is_chairman": True,
                "join_date": "2024-01-31",
                "payment_start_date": "2024-02-01",
                "contact_details": {"id": 2, "first_name": "Max", "is_company": False, "contact_details_groups": []},
                "member_groups": ["https://easyverein.com/api/v3.0/member-group-assignment/3"],
            },
            context=V3,
        )
        assert member.isChairman is True
        assert member.joinDate == datetime.date(2024, 1, 31)
        assert member.paymentStartDate == datetime.date(2024, 2, 1)
        assert isinstance(member.contactDetails, ContactDetails)
        assert member.contactDetails.firstName == "Max"
        assert member.contactDetails.isCompany is False
        assert member.memberGroups and len(member.memberGroups) == 1

    def test_parse_v2_response_unchanged(self):
        details = ContactDetails.model_validate({"id": 2, "firstName": "Max", "_isCompany": True}, context=V2)
        assert details.firstName == "Max"
        assert details.isCompany is True

        # Without context, v2.0 naming is assumed
        assert CustomField.model_validate({"selectOptions": [{"value": "A"}]}).selectOptions

    def test_serialize_create_model(self):
        model = ContactDetailsCreate(firstName="Max", familyName="Mustermann", isCompany=False)
        kwargs = {"exclude_none": True, "exclude_unset": True, "by_alias": True}
        assert model.model_dump(**kwargs, context=V2) == {
            "firstName": "Max",
            "familyName": "Mustermann",
            "_isCompany": False,
        }
        assert model.model_dump(**kwargs, context=V3) == {
            "first_name": "Max",
            "family_name": "Mustermann",
            "is_company": False,
        }

    def test_serialize_action_model(self):
        dump = MemberSetLsb(lsbSport=["1"]).model_dump(by_alias=True, context=V3)
        assert dump == {"lsb_sport": ["1"]}

    def test_wire_name(self):
        assert InvoiceCreate.wire_name("invoiceItems", "v2.0") == "invoiceItems"
        assert InvoiceCreate.wire_name("invoiceItems", "v3.0") == "invoice_items"
        assert ContactDetails.wire_name("isCompany", "v2.0") == "_isCompany"
        assert ContactDetails.wire_name("isCompany", "v3.0") == "is_company"


class TestFilterTranslation:
    @staticmethod
    def dump(model, context):
        return model.model_dump(exclude_unset=True, exclude_none=True, by_alias=True, context=context)

    def test_filter_v3_names(self):
        search = MemberFilter(
            isChairman=True, joinDate__gte=datetime.date(2024, 1, 1), memberGroups__not=[1, 2], id__in=[3]
        )
        assert self.dump(search, V3) == {
            "is_chairman": True,
            "join_date__gte": "2024-01-01",
            "member_groups__ne": "1,2",
            "id__in": "3",
        }
        assert self.dump(search, V2) == {
            "_isChairman": True,
            "joinDate__gte": "2024-01-01",
            "memberGroups__not": "1,2",
            "id__in": "3",
        }

    def test_filter_renames(self):
        assert self.dump(InvoiceItemFilter(relatedInvoice__not=1), V3) == {"related_invoice__ne": 1}
        assert self.dump(ContactDetailsFilter(isReferencedByOrgUser=True), V3) == {"is_referenced_by_member": True}
        assert self.dump(BookingFilter(bookingprojectassignment__not="1", billingId__isempty=True), V3) == {
            "booking_project_assignment_ne": "1",
            "billing_id": True,
        }
        assert self.dump(InvoiceFilter(usesessionfilter=True, customfilter=1), V3) == {
            "use_session_filter": True,
            "custom_filter": 1,
        }

    def test_invoice_date_it_happened_filter(self):
        search = InvoiceFilter(dateItHappened__gt=datetime.date(2024, 1, 1))
        assert self.dump(search, V2) == {"dateItHappend__gt": "2024-01-01"}
        assert self.dump(search, V3) == {"date_it_happend__gt": "2024-01-01"}

    def test_removed_filter_raises(self):
        with pytest.raises(PydanticSerializationError, match="not supported by API v3.0"):
            self.dump(InvoiceFilter(deleted=True), V3)
        assert self.dump(InvoiceFilter(deleted=True), V2) == {"deleted": True}


class TestClient:
    def test_list_params(self):
        api = EasyvereinAPI("dummy", api_version="v3.0")
        params = api.c.list_params(
            query="{id,invNumber}", search=InvoiceFilter(isDraft=False, ordering="-invNumber"), limit=10, page=2
        )
        assert params == {
            "limit": 10,
            "page": 2,
            "show_count": True,
            "query": "{id,inv_number}",
            "is_draft": False,
            "ordering": "-inv_number",
        }

        api = EasyvereinAPI("dummy", api_version="v2.0")
        params = api.c.list_params(query="{id,invNumber}", search=InvoiceFilter(isDraft=False, ordering="-invNumber"))
        assert params == {
            "limit": None,
            "page": None,
            "showCount": True,
            "query": "{id,invNumber}",
            "isDraft": False,
            "ordering": "-invNumber",
        }

    def test_sub_endpoints(self):
        v2 = EasyvereinAPI("dummy", api_version="v2.0")
        assert v2.member.custom_field(5).endpoint_name == "member/5/custom-fields"
        assert v2.member.custom_field(5).scope_params == {}
        assert v2.member.member_group(5).endpoint_name == "member/5/groups"
        assert v2.custom_field.select_option(7).endpoint_name == "custom-field/7/select-options"
        assert v2.invoice.scope_params == {}

        v3 = EasyvereinAPI("dummy", api_version="v3.0")
        assert v3.member.custom_field(5).endpoint_name == "member-custom-field-assignment"
        assert v3.member.custom_field(5).scope_params == {"user_object": 5}
        assert v3.member.member_group(5).endpoint_name == "member-group-assignment"
        assert v3.member.member_group(5).scope_params == {"user_object": 5}
        assert v3.custom_field.select_option(7).endpoint_name == "select-option"
        assert v3.custom_field.select_option(7).scope_params == {"custom_field": 7}

    def test_api_versions(self):
        with pytest.raises(ValueError, match="no longer supported"):
            EasyvereinAPI("dummy", api_version="v1.7")
        with pytest.raises(ValueError, match="not supported"):
            EasyvereinAPI("dummy", api_version="v4.0")
        EasyvereinAPI("dummy", api_version="v3.0", token_refresh_callback=lambda: None)
