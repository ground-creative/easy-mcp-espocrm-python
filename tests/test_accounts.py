import os
import sys
from core.utils.state import global_state
from app.tools.espo_list_accounts import espo_list_accounts_tool
from app.tools.espo_create_account import espo_create_account_tool
from app.tools.espo_delete_account import espo_delete_account_tool
from app.tools.espo_get_account import espo_get_account_tool
from app.tools.espo_update_account import espo_update_account_tool

# from app.tools.espo_relate_contact_to_account import espo_relate_contact_to_account_tool
# from app.tools.espo_unrelate_contact_from_account import (
#    espo_unrelate_contact_from_account_tool,
# )
# from app.tools.espo_list_account_contacts import espo_list_account_contacts_tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_espo_list_leads_tool(api_key_setup, setup_test_account):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    result = espo_list_accounts_tool()

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]

    assert "list" in data and isinstance(data["list"], list)
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1


def test_espo_search_accounts_tool(api_key_setup, setup_test_account):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    search_term = "Test"
    result = espo_list_accounts_tool(text_filter=search_term)

    assert isinstance(result, dict)
    assert "data" in result and isinstance(result["data"], dict)

    data = result["data"]
    assert "list" in data and isinstance(data["list"], list)

    fixture_id = setup_test_account["data"]["id"]
    ids = [item.get("id") for item in data["list"] if isinstance(item, dict)]
    assert (
        fixture_id in ids
    ), f"Created account id {fixture_id} not found in search results"


def test_espo_create_and_delete_account_tool(api_key_setup):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

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

    delete = espo_delete_account_tool(account_id=result["data"]["id"])

    assert isinstance(delete, dict)
    assert "status_code" in delete and delete["status_code"] == 200
    assert "ok" in delete and delete["ok"] is True


def test_espo_get_account_tool(api_key_setup, setup_test_account):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    account_id = setup_test_account["data"]["id"]
    result = espo_get_account_tool(account_id=account_id)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True
    assert "data" in result and isinstance(result["data"], dict)
    assert result["data"]["id"] == account_id


def test_espo_update_account_tool(api_key_setup, setup_test_account):
    """Update the fixture account and verify the changes persisted."""
    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    account_id = setup_test_account["data"]["id"]
    industry = "Architecture"
    new_description = "Updated by automated test"

    res = espo_update_account_tool(
        account_id=account_id, industry=industry, description=new_description
    )
    assert isinstance(res, dict)
    assert "status_code" in res and res["status_code"] == 200
    assert "ok" in res and res["ok"] is True

    # Fetch lead to verify updates
    get_res = espo_get_account_tool(account_id=account_id)
    assert isinstance(get_res, dict)
    assert "status_code" in get_res and get_res["status_code"] == 200
    assert "ok" in get_res and get_res["ok"] is True
    assert "data" in get_res and isinstance(get_res["data"], dict)
    assert get_res["data"].get("industry") == industry
    assert get_res["data"].get("description") == new_description


def test_espo_filter_by_email(api_key_setup, setup_test_account):

    is_api_key_set = global_state.get(
        "middleware.AuthenticationMiddleware.is_authenticated"
    )
    assert is_api_key_set, "No API key set in env file."

    fixture_email = setup_test_account["data"].get("emailAddress")
    assert fixture_email, "Fixture did not provide an emailAddress"

    where = [{"type": "equals", "attribute": "emailAddress", "value": fixture_email}]
    result = espo_list_accounts_tool(where_group=where, max_size=50)

    assert isinstance(result, dict)
    assert "status_code" in result and result["status_code"] == 200
    assert "ok" in result and result["ok"] is True

    data = result.get("data") or {}
    assert "total" in data and isinstance(data["total"], int)
    assert data["total"] >= 1

    items = data.get("list") or []
    assert isinstance(items, list)

    fixture_id = setup_test_account["data"].get("id")
    emails = [it.get("emailAddress") for it in items if isinstance(it, dict)]
    ids = [it.get("id") for it in items if isinstance(it, dict)]
    assert (
        fixture_email in emails or fixture_id in ids
    ), f"Fixture account not found by email {fixture_email} or id {fixture_id}"


# def test_relate_and_unrelate_contact_to_account(
#    api_key_setup, setup_test_contact, setup_test_account
# ):
#    """
#    Test relating a Contact to an Account and then unrelating it.
#    """
# Ensure API key is set
#    assert global_state.get(
#        "middleware.AuthenticationMiddleware.is_authenticated"
#    ), "No API key set"

#    contact_id = setup_test_contact["data"]["id"]
#    account_id = setup_test_account["data"]["id"]

# Step 1: Relate the lead to the campaign
#    relate_result = espo_relate_contact_to_account_tool(
#        account_id=account_id, contact_id=contact_id
#    )
#    assert isinstance(relate_result, dict)
#    assert relate_result.get("status_code") == 200
#    assert relate_result.get("ok") is True

# Step 2: Verify the contact appears in the account's contacts list
#    list_result = espo_list_account_contacts_tool(account_id=account_id)
#    assert isinstance(list_result, dict)
#    assert list_result.get("status_code") == 200
#    assert list_result.get("ok") is True
#    contacts_list = list_result.get("data", {}).get("list", [])
#    contact_ids = [c.get("id") for c in contacts_list if isinstance(c, dict)]
#    assert (
#        contact_id in contact_ids
#    ), f"Contact {contact_id} not found in account {account_id} contacts list"

# Step 3: Unrelate the contact from the account
#    unrelate_result = espo_unrelate_contact_from_account_tool(
#        account_id=account_id, contact_id=contact_id
#    )
#    assert isinstance(unrelate_result, dict)
#    assert unrelate_result.get("status_code") == 200
#    assert unrelate_result.get("ok") is True

# Step 4: Verify the contact no longer appears in the account's contacts list
#    list_after_unrelate = espo_list_account_contacts_tool(account_id=account_id)
#    assert isinstance(list_after_unrelate, dict)
#    assert list_after_unrelate.get("status_code") == 200
#    contacts_list_after = list_after_unrelate.get("data", {}).get("list", [])
#    contact_ids_after = [
#        c.get("id") for c in contacts_list_after if isinstance(c, dict)
#    ]
#    assert (
#        contact_id not in contact_ids_after
#    ), f"Contact {contact_id} still found in account {account_id} contacts list after unrelate"
