import os
import sys
from core.utils.state import global_state
from app.tools.espo_list_target_lists import espo_list_target_lists_tool
from app.tools.espo_create_target_list import espo_create_target_list_tool
from app.tools.espo_delete_target_list import espo_delete_target_list_tool
from app.tools.espo_get_target_list import espo_get_target_list_tool
from app.tools.espo_update_target_list import espo_update_target_list_tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_espo_list_target_lists_tool(api_key_setup, setup_test_target_list):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = espo_list_target_lists_tool(max_size=2)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1


def test_espo_search_target_lists_tool(api_key_setup, setup_test_target_list):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "Test"
    result = espo_list_target_lists_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)

    fixture_id = setup_test_target_list["data"]["id"]
    ids = [item.get("id") for item in data["list"] if isinstance(item, dict)]
    assert (
        fixture_id in ids
    ), f"Created target list id {fixture_id} not found in search results"


def test_espo_create_and_delete_target_list_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    target_list_data = {
        "name": "Test",
        "description": "sample target list",
        "skip_duplicate_check": True,
    }
    result = espo_create_target_list_tool(**target_list_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200

    delete = espo_delete_target_list_tool(target_list_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


def test_espo_get_target_list_tool(api_key_setup, setup_test_target_list):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    target_list_id = setup_test_target_list["data"]["id"]
    result = espo_get_target_list_tool(target_list_id=target_list_id)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and isinstance(result["data"], dict)
    assert result["data"]["id"] == target_list_id


def test_espo_update_target_list_tool(api_key_setup, setup_test_target_list):
    """Update the fixture target list and verify the changes persisted."""
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    target_list_id = setup_test_target_list["data"]["id"]
    new_name = "QA Updated Name"

    res = espo_update_target_list_tool(target_list_id=target_list_id, name=new_name)
    assert isinstance(res, dict)
    assert "status_code" in res and res["status_code"] == 200
    assert "ok" in res and res["ok"] is True

    # Fetch lead to verify updates
    get_res = espo_get_target_list_tool(target_list_id=target_list_id)
    assert isinstance(get_res, dict)
    assert "status_code" in get_res and get_res["status_code"] == 200
    assert "ok" in get_res and get_res["ok"] is True
    assert "data" in get_res and isinstance(get_res["data"], dict)
    assert get_res["data"].get("name") == new_name
