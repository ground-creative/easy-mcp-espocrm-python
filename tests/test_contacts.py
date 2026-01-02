import os
import sys
from core.utils.state import global_state
from app.tools.list_contacts import list_contacts_tool
from app.tools.create_contact import create_contact_tool
from app.tools.delete_contact import delete_contact_tool
from app.tools.update_contact import update_contact_tool
from app.tools.get_contact import get_contact_tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_list_contacts_tool(api_key_setup, setup_test_contact):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = list_contacts_tool(max_size=2)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1


def test_search_contacts_tool(api_key_setup, setup_test_contact):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "Test"
    result = list_contacts_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)

    fixture_id = setup_test_contact["data"]["id"]
    ids = [item.get("id") for item in data["list"] if isinstance(item, dict)]
    assert (
        fixture_id in ids
    ), f"Created contact id {fixture_id} not found in search results"


def test_create_and_delete_contact_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    contact_data = {
        "first_name": "Test",
        "last_name": "Lead",
        "email_address": "test.lead@example.com",
        "skip_duplicate_check": True,
    }
    result = create_contact_tool(**contact_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200

    delete = delete_contact_tool(contact_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


def test_get_contact_tool(api_key_setup, setup_test_contact):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    contact_id = setup_test_contact["data"]["id"]
    result = get_contact_tool(contact_id=contact_id)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and isinstance(result["data"], dict)
    assert result["data"]["id"] == contact_id


def test_update_contact_tool(api_key_setup, setup_test_contact):
    """Update the fixture contact and verify the changes persisted."""
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    contact_id = setup_test_contact["data"]["id"]

    # Fields to update
    new_first_name = "QA_First"
    new_last_name = "QA_Last"
    new_description = "Updated by automated test"

    # Call update tool
    res = update_contact_tool(
        contact_id=contact_id,
        first_name=new_first_name,
        last_name=new_last_name,
        description=new_description,
    )

    # Validate update call response
    assert isinstance(res, dict)
    assert res.get("status_code") == 200
    assert res.get("ok") is True

    # Fetch contact to verify changes
    get_res = get_contact_tool(contact_id=contact_id)
    assert isinstance(get_res, dict)
    assert get_res.get("status_code") == 200
    assert get_res.get("ok") is True
    assert isinstance(get_res.get("data"), dict)

    data = get_res["data"]
    assert data.get("firstName") == new_first_name
    assert data.get("lastName") == new_last_name
    assert data.get("description") == new_description


def test_filter_by_email(api_key_setup, setup_test_contact):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    fixture_email = setup_test_contact["data"].get("emailAddress")
    assert fixture_email, "Fixture did not provide an emailAddress"

    where = [{"type": "equals", "attribute": "emailAddress", "value": fixture_email}]
    result = list_contacts_tool(where_group=where, max_size=50)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    data = result.get("data") or {}
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1

    items = data.get("list") or []
    assert isinstance(items, list)

    fixture_id = setup_test_contact["data"].get("id")
    emails = [it.get("emailAddress") for it in items if isinstance(it, dict)]
    ids = [it.get("id") for it in items if isinstance(it, dict)]
    assert (
        fixture_email in emails or fixture_id in ids
    ), f"Fixture contact not found by email {fixture_email} or id {fixture_id}"
