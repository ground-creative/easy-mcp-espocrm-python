import os
import sys
from core.utils.state import global_state
from app.tools.list_leads import list_leads_tool
from app.tools.create_lead import create_lead_tool
from app.tools.delete_lead import delete_lead_tool
from app.tools.get_lead import get_lead_tool
from app.tools.update_lead import update_lead_tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_list_leads_tool(api_key_setup, setup_test_lead):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = list_leads_tool(max_size=2)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1


def test_search_leads_tool(api_key_setup, setup_test_lead):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "Test"
    result = list_leads_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)

    fixture_id = setup_test_lead["data"]["id"]
    ids = [item.get("id") for item in data["list"] if isinstance(item, dict)]
    assert (
        fixture_id in ids
    ), f"Created lead id {fixture_id} not found in search results"


def test_create_and_delete_lead_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    lead_data = {
        "first_name": "Test",
        "last_name": "Lead",
        "email_address": "test.lead@example.com",
        "skip_duplicate_check": True,
    }
    result = create_lead_tool(**lead_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200

    delete = delete_lead_tool(lead_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


def test_get_lead_tool(api_key_setup, setup_test_lead):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    lead_id = setup_test_lead["data"]["id"]
    result = get_lead_tool(lead_id=lead_id)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and isinstance(result["data"], dict)
    assert result["data"]["id"] == lead_id


def test_update_lead_tool(api_key_setup, setup_test_lead):
    """Update the fixture lead and verify the changes persisted."""
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    lead_id = setup_test_lead["data"]["id"]
    new_title = "QA Updated Title"
    new_description = "Updated by automated test"

    res = update_lead_tool(
        lead_id=lead_id, title=new_title, description=new_description
    )
    assert isinstance(res, dict)
    assert "status_code" in res and res["status_code"] == 200
    assert "ok" in res and res["ok"] is True

    # Fetch lead to verify updates
    get_res = get_lead_tool(lead_id=lead_id)
    assert isinstance(get_res, dict)
    assert "status_code" in get_res and get_res["status_code"] == 200
    assert "ok" in get_res and get_res["ok"] is True
    assert "data" in get_res and isinstance(get_res["data"], dict)
    assert get_res["data"].get("title") == new_title
    assert get_res["data"].get("description") == new_description


def test_filter_by_email(api_key_setup, setup_test_lead):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    fixture_email = setup_test_lead["data"].get("emailAddress")
    assert fixture_email, "Fixture did not provide an emailAddress"

    where = [{"type": "equals", "attribute": "emailAddress", "value": fixture_email}]
    result = list_leads_tool(where_group=where, max_size=50)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    data = result.get("data") or {}
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1

    items = data.get("list") or []
    assert isinstance(items, list)

    fixture_id = setup_test_lead["data"].get("id")
    emails = [it.get("emailAddress") for it in items if isinstance(it, dict)]
    ids = [it.get("id") for it in items if isinstance(it, dict)]
    assert (
        fixture_email in emails or fixture_id in ids
    ), f"Fixture lead not found by email {fixture_email} or id {fixture_id}"
