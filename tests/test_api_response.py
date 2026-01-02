import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from core.utils.state import global_state
from core.utils.env import EnvConfig
from app.tools.list_leads import list_leads_tool
from app.utils.espo_helpers import EspoAPI, build_espo_params


def test_api_error_response():

    api_key = "invalidapikey"
    api_address = EnvConfig.get("TEST_API_ADDRESS")
    client = EspoAPI(api_address, api_key)
    result = client.call_api("GET", "Lead")
    assert isinstance(result, dict)
    assert "error" in result
    assert "status_code" != 200
