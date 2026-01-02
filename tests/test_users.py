import os
import sys
import pytest
from core.utils.state import global_state
from app.tools.list_users import list_users_tool
from app.tools.get_user import get_user_tool

# from app.tools.update_user import update_user_tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_list_users_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = list_users_tool(max_size=2)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    # assert data["total"] >= 1


def test_search_leads_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "admin"
    result = list_users_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)
    assert data["total"] >= 1


def test_get_user_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "admin"
    result = list_users_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)
    assert data["total"] >= 1

    fixture_id = data["list"][0]["id"]
    get_result = get_user_tool(user_id=fixture_id)
    assert isinstance(get_result, dict)
    assert "status_code" in get_result and get_result["status_code"] == 200
    assert "ok" in get_result and get_result["ok"] is True


# @pytest.mark.skip(reason="WE cannot edit other users but the api user.")
# def test_update_user_tool(api_key_setup):
#    """Update the fixture lead and verify the changes persisted."""
#    is_api_key_set = global_state.get(
#        "middleware.AuthenticationMiddleware.is_authenticated"
#    )
#    assert is_api_key_set, "No API key set in env file."

#    search_term = "admin"
#    result = list_users_tool(text_filter=search_term)

#    assert isinstance(result, dict)
#    assert "data" in result and isinstance(result["data"], dict)

#    data = result["data"]
#    assert "list" in data and isinstance(data["list"], list)
#    assert data["total"] >= 1

#    fixture_id = data["list"][0]["id"]
#    old_title = data["list"][0].get("title", "")
#    new_title = "QA Updated User Title"
#    res = update_user_tool(user_id=fixture_id, title=new_title)
#    assert isinstance(res, dict)
#    assert "status_code" in res and res["status_code"] == 200
#    assert "ok" in res and res["ok"] is True

#    update = update_user_tool(user_id=fixture_id, title=old_title)
#    assert isinstance(update, dict)
#    assert "status_code" in update and update["status_code"] == 200
#    assert "ok" in update and update["ok"] is True
