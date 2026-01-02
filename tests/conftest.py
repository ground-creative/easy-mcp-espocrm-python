import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from core.utils.state import global_state
from core.utils.env import EnvConfig
from app.tools.create_lead import create_lead_tool
from app.tools.delete_lead import delete_lead_tool
from app.tools.create_campaign import create_campaign_tool
from app.tools.delete_campaign import delete_campaign_tool
from app.tools.create_contact import create_contact_tool
from app.tools.delete_contact import delete_contact_tool
from app.tools.create_account import create_account_tool
from app.tools.delete_account import delete_account_tool
from app.tools.create_email import create_email_tool
from app.tools.delete_email import delete_email_tool
from app.tools.create_target_list import create_target_list_tool
from app.tools.delete_target_list import delete_target_list_tool
from app.tools.delete_call import delete_call_tool
from app.tools.create_call import create_call_tool
from app.tools.list_users import list_users_tool


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
    result = create_lead_tool(**lead_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = delete_lead_tool(lead_id=result["data"]["id"])

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
    result = create_campaign_tool(**campaign_data)

    # Basic assertions to ensure creation succeeded
    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and "id" in result["data"]

    # Provide the campaign data to tests
    yield result

    # Teardown: delete the test campaign
    delete_result = delete_campaign_tool(campaign_id=result["data"]["id"])

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
    result = create_contact_tool(**contact_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = delete_contact_tool(contact_id=result["data"]["id"])

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
    result = create_account_tool(**account_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = delete_account_tool(account_id=result["data"]["id"])

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
    result = create_email_tool(**email_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = delete_email_tool(email_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


@pytest.fixture(scope="module")
def setup_test_target_list():

    target_list_data = {
        "name": "Test Target List",
    }
    result = create_target_list_tool(**target_list_data)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = delete_target_list_tool(target_list_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


@pytest.fixture(scope="module")
def setup_test_call():

    users = list_users_tool()

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
    result = create_call_tool(**call_data)
    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    yield result

    delete = delete_call_tool(call_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True
