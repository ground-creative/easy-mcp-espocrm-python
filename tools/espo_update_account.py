from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Accounts")
@doc_name("Update Account")
def espo_update_account_tool(
    account_id: str,
    name: Annotated[
        Optional[str], Field(description="Account name (<=249 chars)")
    ] = None,
    website: Annotated[
        Optional[str], Field(description="Website (<=255 chars)")
    ] = None,
    email_address: Annotated[
        Optional[str], Field(description="Primary email address (<=255 chars)")
    ] = None,
    email_address_data: Annotated[
        Optional[List[Dict[str, Any]]], Field(description="Multiple email addresses")
    ] = None,
    phone_number: Annotated[
        Optional[str], Field(description="Primary phone number (<=36 chars)")
    ] = None,
    phone_number_data: Annotated[
        Optional[List[Dict[str, Any]]], Field(description="Multiple phone numbers")
    ] = None,
    type: Annotated[
        Optional[str],
        Field(description="Account type (Customer, Investor, Partner, Reseller)"),
    ] = None,
    industry: Annotated[
        Optional[str], Field(description="Industry (see allowed values)")
    ] = None,
    sic_code: Annotated[
        Optional[str], Field(description="SIC Code (<=40 chars)")
    ] = None,
    billing_address_street: Annotated[
        Optional[str], Field(description="Billing street (<=255 chars)")
    ] = None,
    billing_address_city: Annotated[
        Optional[str], Field(description="Billing city (<=100 chars)")
    ] = None,
    billing_address_state: Annotated[
        Optional[str], Field(description="Billing state (<=100 chars)")
    ] = None,
    billing_address_country: Annotated[
        Optional[str], Field(description="Billing country (<=100 chars)")
    ] = None,
    billing_address_postal_code: Annotated[
        Optional[str], Field(description="Billing postal code (<=40 chars)")
    ] = None,
    shipping_address_street: Annotated[
        Optional[str], Field(description="Shipping street (<=255 chars)")
    ] = None,
    shipping_address_city: Annotated[
        Optional[str], Field(description="Shipping city (<=100 chars)")
    ] = None,
    shipping_address_state: Annotated[
        Optional[str], Field(description="Shipping state (<=100 chars)")
    ] = None,
    shipping_address_country: Annotated[
        Optional[str], Field(description="Shipping country (<=100 chars)")
    ] = None,
    shipping_address_postal_code: Annotated[
        Optional[str], Field(description="Shipping postal code (<=40 chars)")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Account description / notes")
    ] = None,
    campaign_id: Annotated[Optional[str], Field(description="Campaign ID")] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned user ID")
    ] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
    target_lists_ids: Annotated[
        Optional[List[str]], Field(description="Target list IDs")
    ] = None,
    target_list_id: Annotated[
        Optional[str], Field(description="Primary target list ID")
    ] = None,
    email_address_is_opted_out: Annotated[
        Optional[bool], Field(description="Email opted out flag")
    ] = None,
    email_address_is_invalid: Annotated[
        Optional[bool], Field(description="Email invalid flag")
    ] = None,
    phone_number_is_opted_out: Annotated[
        Optional[bool], Field(description="Phone opted out flag")
    ] = None,
    phone_number_is_invalid: Annotated[
        Optional[bool], Field(description="Phone invalid flag")
    ] = None,
    version_number: Annotated[
        Optional[str], Field(description="Version number for optimistic locking")
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(
            description="Custom EspoCRM fields (must start with `c`, e.g. cCustomField)"
        ),
    ] = None,
) -> Dict:
    """
    Update an existing Account in EspoCRM.

    Updates an Account record by `account_id`. Only provided fields are sent to EspoCRM.
    Fields left as None will not overwrite existing values.

    Args:
    - `account_id` (str): ID of the Account record to update.
    - `name` (Optional[str]): Account name.
    - `website` (Optional[str]): Website.
    - `email_address` (Optional[str]): Primary email.
    - `email_address_data` (Optional[List[Dict[str, Any]]]): Multiple email objects.
    - `phone_number` (Optional[str]): Primary phone.
    - `phone_number_data` (Optional[List[Dict[str, Any]]]): Multiple phone objects.
    - `type` (Optional[str]): Account type.
    - `industry` (Optional[str]): Industry.
    - `sic_code` (Optional[str]): SIC code.
    - Billing & Shipping address fields.
    - `description` (Optional[str]): Description.
    - `campaign_id` (Optional[str]): Campaign ID.
    - `assigned_user_id` (Optional[str]): Assigned user ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `target_lists_ids` (Optional[List[str]]): Target list IDs.
    - `target_list_id` (Optional[str]): Primary target list ID.
    - Opt-out / invalid flags.
    - `version_number` (Optional[str]): Optimistic locking version.
    - `custom_fields` (Optional[Dict[str, Any]]): EspoCRM custom fields.

    Example Requests:
    - Update an account's name and website:
    espo_update_account_tool(account_id="abc123", name="Acme Inc", website="https://acme.com")
    - Update phone number and industry:
    espo_update_account_tool(account_id="abc123", phone_number="+123456789", industry="Technology")
    - Update custom fields:
    espo_update_account_tool(account_id="abc123", custom_fields={"c_score": 92})

    Returns:
    - A structured dict containing: status_code, ok, data, error, error_type.
    """
    logger.info(
        f"Request received to update account {account_id} with params: {locals()}"
    )

    # Core: check access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Core: build params
    params = build_espo_params(locals(), exclude={"account_id", "auth_response"})

    if custom_fields:
        params.update(custom_fields)

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Core: call API
    result = client.call_api("PATCH", f"Account/{account_id}", params=params)
    logger.debug(f"EspoCRM update account result: {result}")
    return result
