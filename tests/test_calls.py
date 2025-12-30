import os
import sys
from core.utils.state import global_state
from app.tools.espo_list_calls import espo_list_calls_tool
from app.tools.espo_create_call import espo_create_call_tool
from app.tools.espo_delete_call import espo_delete_call_tool
from app.tools.espo_get_call import espo_get_call_tool
from app.tools.espo_update_call import espo_update_call_tool

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
