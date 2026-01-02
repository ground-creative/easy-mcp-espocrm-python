import os
import sys
from core.utils.state import global_state
from app.tools.espo_list_calls import espo_list_calls_tool
from app.tools.espo_create_call import espo_create_call_tool
from app.tools.espo_delete_call import espo_delete_call_tool
from app.tools.espo_get_call import espo_get_call_tool
from app.tools.espo_update_call import espo_update_call_tool
from app.tools.espo_list_users import espo_list_users_tool


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_espo_list_calls_tool(api_key_setup, setup_test_call):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = espo_list_calls_tool(max_size=2)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1


def test_espo_search_calls_tool(api_key_setup, setup_test_call):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "Test"
    result = espo_list_calls_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)

    fixture_id = setup_test_call["data"]["id"]
    ids = [item.get("id") for item in data["list"] if isinstance(item, dict)]
    assert (
        fixture_id in ids
    ), f"Created account id {fixture_id} not found in search results"


def test_espo_create_and_delete_call_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    users = espo_list_users_tool()

    assert isinstance(users, dict)
    assert "data" in users and isinstance(users["data"], dict)
    assert "list" in users["data"] and isinstance(users["data"]["list"], list)
    assert len(users["data"]["list"]) >= 1, "No users found in EspoCRM instance."

    call_data = {
        "name": "Test Call",
        "status": "Planned",
        "description": "Test call description",
        "date_start": "2026-11-29 12:34:56",
        "date_end": "2026-11-29 12:34:56",
        "assigned_user_id": users["data"]["list"][0]["id"],
    }
    result = espo_create_call_tool(**call_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200

    delete = espo_delete_call_tool(call_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


def test_espo_get_call_tool(api_key_setup, setup_test_call):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    call_id = setup_test_call["data"]["id"]
    result = espo_get_call_tool(call_id=call_id)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and isinstance(result["data"], dict)
    assert result["data"]["id"] == call_id


def test_espo_update_call_tool(api_key_setup, setup_test_call):
    """Update the fixture call and verify the changes persisted."""
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    call_id = setup_test_call["data"]["id"]
    new_description = "Updated by automated test"

    res = espo_update_call_tool(call_id=call_id, description=new_description)
    assert isinstance(res, dict)
    assert "status_code" in res and res["status_code"] == 200
    assert "ok" in res and res["ok"] is True

    # Fetch lead to verify updates
    get_res = espo_get_call_tool(call_id=call_id)
    assert isinstance(get_res, dict)
    assert "status_code" in get_res and get_res["status_code"] == 200
    assert "ok" in get_res and get_res["ok"] is True
    assert "data" in get_res and isinstance(get_res["data"], dict)
    assert get_res["data"].get("description") == new_description
