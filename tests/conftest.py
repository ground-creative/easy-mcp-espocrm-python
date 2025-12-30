import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from core.utils.state import global_state
from core.utils.env import EnvConfig
from app.tools.espo_create_lead import espo_create_lead_tool
from app.tools.espo_delete_lead import espo_delete_lead_tool

@pytest.fixture(scope="module")
def api_key_setup():
    global_state.set("middleware.AuthenticationMiddleware.is_authenticated", False, True)

    api_key = EnvConfig.get("TEST_API_KEY")
    api_address = EnvConfig.get("TEST_API_ADDRESS")

    assert api_key, "TEST_API_KEY is not set in env file."
    assert api_address, "TEST_API_ADDRESS is not set in env file."

    global_state.set("middleware.AuthenticationMiddleware.is_authenticated", True, True)
    global_state.set("api_key", api_key, True)
    global_state.set("api_address", api_address, True)

    return api_key, api_address

@pytest.fixture(scope="module")
def setup_test_lead():

    lead_data = {
        "first_name": "Test",
        "last_name": "Lead",
        "email_address": "test.lead@example.com",
        "skip_duplicate_check": True,
    }
    result = espo_create_lead_tool(**lead_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = espo_delete_lead_tool(lead_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True
