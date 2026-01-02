import os
import sys
from core.utils.state import global_state
from app.tools.list_emails import list_emails_tool
from app.tools.create_email import create_email_tool
from app.tools.delete_email import delete_email_tool
from app.tools.get_email import get_email_tool
from app.tools.update_email import update_email_tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_list_emails_tool(api_key_setup, setup_test_email):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = list_emails_tool(max_size=2)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    # assert data["total"] >= 1


def test_search_emails_tool(api_key_setup, setup_test_email):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "Proposal draft"
    result = list_emails_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)

    fixture_id = setup_test_email["data"]["id"]
    ids = [item.get("id") for item in data["list"] if isinstance(item, dict)]
    assert (
        fixture_id in ids
    ), f"Created email id {fixture_id} not found in search results"


def test_create_and_delete_email_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    email_data = {
        "name": "Draft email",
        "subject": "Proposal draft",
        "from_": "John Doe <john@example.com>",
        "to": "client@example.com",
        "is_html": True,
        "status": "Draft",
    }
    result = create_email_tool(**email_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200

    delete = delete_email_tool(email_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


def test_get_email_tool(api_key_setup, setup_test_email):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    email_id = setup_test_email["data"]["id"]
    result = get_email_tool(email_id=email_id)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and isinstance(result["data"], dict)
    assert result["data"]["id"] == email_id


def test_update_email_tool(api_key_setup, setup_test_email):
    """Update the fixture email and verify the changes persisted."""
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    email_id = setup_test_email["data"]["id"]
    new_subject = "QA Updated Subject"

    res = update_email_tool(email_id=email_id, subject=new_subject)
    assert isinstance(res, dict)
    assert "status_code" in res and res["status_code"] == 200
    assert "ok" in res and res["ok"] is True

    # Fetch lead to verify updates
    get_res = get_email_tool(email_id=email_id)
    assert isinstance(get_res, dict)
    assert "status_code" in get_res and get_res["status_code"] == 200
    assert "ok" in get_res and get_res["ok"] is True
    assert "data" in get_res and isinstance(get_res["data"], dict)
    assert get_res["data"].get("subject") == new_subject


def test_filter_by_email(api_key_setup, setup_test_email):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    fixture_email = setup_test_email["data"].get("to")
    assert fixture_email, "Fixture did not provide an emailAddress"

    where = [{"type": "equals", "attribute": "to", "value": fixture_email}]
    result = list_emails_tool(where_group=where, max_size=50)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    data = result.get("data") or {}
    assert "total" in data and isinstance(data["total"], int)
    # assert data["total"] >= 1

    items = data.get("list") or []
    assert isinstance(items, list)

    fixture_id = setup_test_email["data"].get("id")
    emails = [it.get("emailAddress") for it in items if isinstance(it, dict)]
    ids = [it.get("id") for it in items if isinstance(it, dict)]
    assert (
        fixture_email in emails or fixture_id in ids
    ), f"Fixture lead not found by email {fixture_email} or id {fixture_id}"
