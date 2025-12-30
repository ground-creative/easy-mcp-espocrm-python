import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from core.utils.state import global_state
from core.utils.env import EnvConfig
from app.tools.espo_create_lead import espo_create_lead_tool
from app.tools.espo_delete_lead import espo_delete_lead_tool
from app.tools.espo_create_campaign import espo_create_campaign_tool
from app.tools.espo_delete_campaign import espo_delete_campaign_tool
from app.tools.espo_create_contact import espo_create_contact_tool
from app.tools.espo_delete_contact import espo_delete_contact_tool
from app.tools.espo_create_account import espo_create_account_tool
from app.tools.espo_delete_account import espo_delete_account_tool
from app.tools.espo_create_email import espo_create_email_tool
from app.tools.espo_delete_email import espo_delete_email_tool
from app.tools.espo_create_target_list import espo_create_target_list_tool
from app.tools.espo_delete_target_list import espo_delete_target_list_tool
from app.tools.espo_delete_call import espo_delete_call_tool
from app.tools.espo_create_call import espo_create_call_tool


@pytest.fixture(scope="module")
def api_key_setup():
    global_state.set(
        "middleware.AuthenticationMiddleware.is_authenticated", False, True
    )

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
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


@pytest.fixture(scope="module")
def setup_test_campaign():
    # Data for creating the test campaign
    campaign_data = {
        "name": "Test Campaign",
        "status": "Planning",
        "type": "Email",
        "skip_duplicate_check": True,
    }

    # Create the campaign
    result = espo_create_campaign_tool(**campaign_data)

    # Basic assertions to ensure creation succeeded
    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and "id" in result["data"]

    # Provide the campaign data to tests
    yield result

    # Teardown: delete the test campaign
    delete_result = espo_delete_campaign_tool(campaign_id=result["data"]["id"])

    # Assertions to ensure deletion succeeded
    assert isinstance(delete_result, dict)
    assert "status_code" in delete_result and delete_result["status_code"] == 200
    assert "ok" in delete_result and delete_result["ok"] is True


@pytest.fixture(scope="module")
def setup_test_contact():

    contact_data = {
        "first_name": "Test",
        "last_name": "Lead",
        "email_address": "test.lead@example.com",
        "skip_duplicate_check": True,
    }
    result = espo_create_contact_tool(**contact_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = espo_delete_contact_tool(contact_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


@pytest.fixture(scope="module")
def setup_test_account():

    account_data = {
        "name": "Test Account",
        "email_address": "test.account@example.com",
        "type": "Customer",
        "industry": "Advertising",
        "skip_duplicate_check": True,
    }
    result = espo_create_account_tool(**account_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = espo_delete_account_tool(account_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


@pytest.fixture(scope="module")
def setup_test_email():

    email_data = {
        "name": "Draft email",
        "subject": "Proposal draft",
        "from_": "John Doe <john@example.com>",
        "to": "client@example.com",
        "is_html": True,
        "status": "Draft",
    }
    result = espo_create_email_tool(**email_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = espo_delete_email_tool(email_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


@pytest.fixture(scope="module")
def setup_test_target_list():

    target_list_data = {
        "name": "Test Target List",
    }
    result = espo_create_target_list_tool(**target_list_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = espo_delete_target_list_tool(target_list_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


@pytest.fixture(scope="module")
def setup_test_call():

    call_data = {
        "name": "string",
        "status": "Planned",
        "description": "Test call description",
    }
    result = espo_create_call_tool(**call_data)
    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = espo_delete_call_tool(call_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True
