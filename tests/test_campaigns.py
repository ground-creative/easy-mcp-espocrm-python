import os
import sys
import time
from core.utils.state import global_state
from app.tools.espo_list_campaigns import espo_list_campaigns_tool
from app.tools.espo_create_campaign import espo_create_campaign_tool
from app.tools.espo_delete_campaign import espo_delete_campaign_tool
from app.tools.espo_get_campaign import espo_get_campaign_tool
from app.tools.espo_update_campaign import espo_update_campaign_tool

# from app.tools.espo_relate_lead_to_campaign import espo_relate_lead_to_campaign_tool
# from app.tools.espo_unrelate_lead_from_campaign import (
#    espo_unrelate_lead_from_campaign_tool,
# )
# from app.tools.espo_list_campaign_leads import espo_list_campaign_leads_tool
# from app.tools.espo_list_campaign_contacts import espo_list_campaign_contacts_tool
# from app.tools.espo_relate_contact_to_campaign import (
#    espo_relate_contact_to_campaign_tool,
# )
# from app.tools.espo_unrelate_contact_from_campaign import (
#    espo_unrelate_contact_from_campaign_tool,
# )

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_espo_list_campaigns_tool(api_key_setup, setup_test_campaign):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = espo_list_campaigns_tool(max_size=2)
    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1


def test_espo_search_campaigns_tool(api_key_setup, setup_test_campaign):
    """
    Test searching/listing campaigns and confirm that the fixture campaign appears in results.
    """
    # Confirm API key is set
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "Test"
    result = espo_list_campaigns_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)

    fixture_id = setup_test_campaign["data"]["id"]
    ids = [item.get("id") for item in data["list"] if isinstance(item, dict)]
    assert (
        fixture_id in ids
    ), f"Created campaign id {fixture_id} not found in search results"


def test_espo_filter_campaign_by_name(api_key_setup, setup_test_campaign):
    """
    Test filtering campaigns by name using where_group filter.
    """
    # Ensure API key is set
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    # Get the fixture campaign name
    fixture_name = setup_test_campaign["data"].get("name")
    assert fixture_name, "Fixture did not provide a name"

    # Build a where_group filter to find campaigns by exact name
    where = [{"type": "equals", "attribute": "name", "value": fixture_name}]
    result = espo_list_campaigns_tool(where_group=where, max_size=50)

    # Basic response checks
    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    data = result.get("data") or {}
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1

    items = data.get("list") or []
    assert isinstance(items, list)

    # Verify fixture campaign is in the results
    fixture_id = setup_test_campaign["data"].get("id")
    names = [it.get("name") for it in items if isinstance(it, dict)]
    ids = [it.get("id") for it in items if isinstance(it, dict)]
    assert (
        fixture_name in names or fixture_id in ids
    ), f"Fixture campaign not found by name '{fixture_name}' or id '{fixture_id}'"


def test_espo_create_and_delete_campaign_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    campaign_data = {
        "name": "Test Campaign",
        "status": "Planning",
        "type": "Email",
        "skip_duplicate_check": True,
    }
    result = espo_create_campaign_tool(**campaign_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200

    delete = espo_delete_campaign_tool(campaign_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


def test_espo_get_campaign_tool(api_key_setup, setup_test_campaign):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    campaign_id = setup_test_campaign["data"]["id"]
    result = espo_get_campaign_tool(campaign_id=campaign_id)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and isinstance(result["data"], dict)
    assert result["data"]["id"] == campaign_id


def test_espo_update_campaign_tool(api_key_setup, setup_test_campaign):
    """Update the fixture campaign and verify the changes persisted."""
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    campaign_id = setup_test_campaign["data"]["id"]
    new_name = "Updated Campaign Name"
    new_description = "Updated by automated test"

    res = espo_update_campaign_tool(
        campaign_id=campaign_id, name=new_name, description=new_description
    )
    assert isinstance(res, dict)
    assert "status_code" in res and res["status_code"] == 200
    assert "ok" in res and res["ok"] is True

    # Fetch campaign to verify updates
    get_res = espo_get_campaign_tool(campaign_id=campaign_id)
    assert isinstance(get_res, dict)
    assert "status_code" in get_res and get_res["status_code"] == 200
    assert "ok" in get_res and get_res["ok"] is True
    assert "data" in get_res and isinstance(get_res["data"], dict)
    assert get_res["data"].get("name") == new_name
    assert get_res["data"].get("description") == new_description


# def test_relate_and_unrelate_lead_to_campaign(
#    api_key_setup, setup_test_lead, setup_test_campaign
# ):
#    """
#    Test relating a Lead to a Campaign and then unrelating it.
#    """

#    # Ensure API key is set
#    assert global_state.get(
#        "middleware.AuthenticationMiddleware.is_authenticated"
#    ), "No API key set"

#    lead_id = setup_test_lead["data"]["id"]
#    campaign_id = setup_test_campaign["data"]["id"]

# Step 1: Relate the lead to the campaign
#    relate_result = espo_relate_lead_to_campaign_tool(
#        campaign_id=campaign_id, lead_id=lead_id
#    )
#    assert isinstance(relate_result, dict)
#    assert relate_result.get("status_code") == 200
#    assert relate_result.get("ok") is True

# Step 2: Verify the lead appears in the campaign's leads list
#    list_result = espo_list_campaign_leads_tool(campaign_id=campaign_id)
#    assert isinstance(list_result, dict)
#    assert list_result.get("status_code") == 200
#    assert list_result.get("ok") is True
#    leads_list = list_result.get("data", {}).get("list", [])
#    lead_ids = [l.get("id") for l in leads_list if isinstance(l, dict)]
#    assert (
#        lead_id in lead_ids
#    ), f"Lead {lead_id} not found in campaign {campaign_id} leads list"

# Step 3: Unrelate the lead from the campaign
#    unrelate_result = espo_unrelate_lead_from_campaign_tool(
#        campaign_id=campaign_id, lead_id=lead_id
#    )
#    assert isinstance(unrelate_result, dict)
#    assert unrelate_result.get("status_code") == 200
#    assert unrelate_result.get("ok") is True

# Step 4: Verify the lead no longer appears in the campaign's leads list
#    list_after_unrelate = espo_list_campaign_leads_tool(campaign_id=campaign_id)
#    assert isinstance(list_after_unrelate, dict)
#    assert list_after_unrelate.get("status_code") == 200
#    leads_list_after = list_after_unrelate.get("data", {}).get("list", [])
#    lead_ids_after = [l.get("id") for l in leads_list_after if isinstance(l, dict)]
#    assert (
#        lead_id not in lead_ids_after
#    ), f"Lead {lead_id} still found in campaign {campaign_id} leads list after unrelate"


# def test_relate_and_unrelate_contact_to_campaign(
#    api_key_setup, setup_test_contact, setup_test_campaign
# ):
#    """
#    Test relating a Contact to a Campaign and then unrelating it.
#    """

# Ensure API key is set
#    assert global_state.get(
#        "middleware.AuthenticationMiddleware.is_authenticated"
#    ), "No API key set"

#    contact_id = setup_test_contact["data"]["id"]
#    campaign_id = setup_test_campaign["data"]["id"]

# Step 1: Relate the contact to the campaign
#    relate_result = espo_relate_contact_to_campaign_tool(
#        campaign_id=campaign_id, contact_id=contact_id
#    )
#    assert isinstance(relate_result, dict)
#    assert relate_result.get("status_code") == 200
#    assert relate_result.get("ok") is True

# Step 2: Verify the contact appears in the campaign's contacts list
#    list_result = espo_list_campaign_contacts_tool(campaign_id=campaign_id)
#    assert isinstance(list_result, dict)
#    assert list_result.get("status_code") == 200
#    assert list_result.get("ok") is True
#    contacts_list = list_result.get("data", {}).get("list", [])
#    contact_ids = [c.get("id") for c in contacts_list if isinstance(c, dict)]
#    assert (
#        contact_id in contact_ids
#    ), f"Contact {contact_id} not found in campaign {campaign_id} contacts list"

# Step 3: Unrelate the contact from the campaign
#    unrelate_result = espo_unrelate_contact_from_campaign_tool(
#        campaign_id=campaign_id, contact_id=contact_id
#    )
#    assert isinstance(unrelate_result, dict)
#    assert unrelate_result.get("status_code") == 200
#    assert unrelate_result.get("ok") is True

# Step 4: Verify the contact no longer appears in the campaign's contacts list
#    list_after_unrelate = espo_list_campaign_contacts_tool(campaign_id=campaign_id)
#    assert isinstance(list_after_unrelate, dict)
#    assert list_after_unrelate.get("status_code") == 200
#    contacts_list_after = list_after_unrelate.get("data", {}).get("list", [])
#    contact_ids_after = [
#        c.get("id") for c in contacts_list_after if isinstance(c, dict)
#    ]
#    assert (
#        contact_id not in contact_ids_after
#    ), f"Contact {contact_id} still found in campaign {campaign_id} contacts list after unrelate"
