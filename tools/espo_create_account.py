from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Accounts")
@doc_name("Create Account")
def espo_create_account_tool(
    name: Annotated[
        Optional[str], Field(description="Account name (<=249 chars)")
    ] = None,
    website: Annotated[
        Optional[str], Field(description="Website (<=255 chars)")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Description / notes")
    ] = None,
    email_address: Annotated[
        Optional[str], Field(description="Primary email (<=255 chars)")
    ] = None,
    email_address_data: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Multiple emails array of objects"),
    ] = None,
    email_address_is_opted_out: Annotated[
        Optional[bool], Field(description="Email opted out")
    ] = None,
    email_address_is_invalid: Annotated[
        Optional[bool], Field(description="Email invalid")
    ] = None,
    phone_number: Annotated[
        Optional[str], Field(description="Primary phone (<=36 chars)")
    ] = None,
    phone_number_data: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Multiple phone numbers array of objects"),
    ] = None,
    phone_number_is_opted_out: Annotated[
        Optional[bool], Field(description="Phone opted out")
    ] = None,
    phone_number_is_invalid: Annotated[
        Optional[bool], Field(description="Phone invalid")
    ] = None,
    type: Annotated[
        Optional[str],
        Field(description="Account category (Customer, Investor, Partner, Reseller)"),
    ] = None,
    industry: Annotated[
        Optional[str], Field(description="Industry (EspoCRM allowed values)")
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
    campaign_id: Annotated[Optional[str], Field(description="Campaign ID")] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned user ID")
    ] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
    target_lists_ids: Annotated[
        Optional[List[str]], Field(description="Target List IDs")
    ] = None,
    target_list_id: Annotated[
        Optional[str], Field(description="Target List ID")
    ] = None,
    email_address_is_opted_out_flag: Annotated[
        Optional[bool], Field(description="emailAddressIsOptedOut")
    ] = None,
    email_address_is_invalid_flag: Annotated[
        Optional[bool], Field(description="emailAddressIsInvalid")
    ] = None,
    phone_number_is_opted_out_flag: Annotated[
        Optional[bool], Field(description="phoneNumberIsOptedOut")
    ] = None,
    phone_number_is_invalid_flag: Annotated[
        Optional[bool], Field(description="phoneNumberIsInvalid")
    ] = None,
    duplicate_source_id: Annotated[
        Optional[str],
        Field(
            description="Record ID of an entity being duplicated. Sent as header 'X-Duplicate-Source-Id'."
        ),
    ] = None,
    skip_duplicate_check: Annotated[
        Optional[bool],
        Field(
            description="Skip duplicate check. Sent as header 'X-Skip-Duplicate-Check' with value 'true' or 'false'."
        ),
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(description="Custom EspoCRM fields (must start with `c`)"),
    ] = None,
) -> Dict:
    """
    Update an existing Account in EspoCRM.

    This tool updates an Account record using common Account fields. Any parameter set to `None` is omitted from
    the request to avoid overwriting existing server values.

    Args:
    - `account_id` (str): ID of the Account record to update.
    - `name` (Optional[str]): Account name (<=249 chars).
    - `website` (Optional[str]): Website (<=255 chars).
    - `description` (Optional[str]): Description / notes.
    - `email_address` (Optional[str]): Primary email (<=255 chars).
    - `email_address_data` (Optional[List[Dict[str, Any]]]): Multiple email objects.
    - `phone_number` (Optional[str]): Primary phone (<=36 chars).
    - `phone_number_data` (Optional[List[Dict[str, Any]]]): Multiple phone objects.
    - `type` (Optional[str]): Account type (Customer, Investor, Partner, Reseller).
    - `industry` (Optional[str]): Industry (see API allowed values).
    - `sic_code` (Optional[str]): SIC Code (<=40 chars).
    - `billing_address_*` / `shipping_address_*` : address fields.
    - `campaign_id`, `assigned_user_id`, `teams_ids`, `target_lists_ids`, `target_list_id`: relations.
    - `email_address_is_opted_out`, `email_address_is_invalid`, `phone_number_is_opted_out`, `phone_number_is_invalid`: opt-out / invalid flags.
    - `version_number` (Optional[str]): Sent as header X-Version-Number for optimistic locking.
    - `custom_fields` (Optional[Dict[str, Any]]): EspoCRM custom fields (prefix `c`).

    Example Requests:
    - Basic:
    espo_update_account_tool(account_id="abc123", name="Acme Corp", website="https://acme.com", email_address="info@acme.com")
    - With multiple emails & phones:
    espo_update_account_tool(account_id="abc123", email_address_data=[{"emailAddress":"info@acme.com","primary":True}], phone_number_data=[{"phoneNumber":"+123","primary":True,"type":"Office"}])
    - With version control:
    espo_update_account_tool(account_id="abc123", name="Acme Corp", version_number="3")
    - With custom fields:
    espo_update_account_tool(account_id="abc123", custom_fields={"c_customer_score":95})

    Returns:
    - A structured dict containing the API response with keys:
    `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to create account with params: {locals()}")

    # Check api key and address are set in headers
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Exclude header-only params from request body
    params = build_espo_params(
        locals(),
        exclude={"duplicate_source_id", "skip_duplicate_check", "auth_response"},
    )

    # Build headers for duplicate handling if provided
    extra_headers = {}
    if duplicate_source_id:
        extra_headers["X-Duplicate-Source-Id"] = str(duplicate_source_id)
    if skip_duplicate_check is not None:
        extra_headers["X-Skip-Duplicate-Check"] = (
            "true" if skip_duplicate_check else "false"
        )

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Call the API
    result = client.call_api(
        "POST",
        "Account",
        params=params,
        extra_headers=extra_headers if extra_headers else None,
    )
    logger.debug(f"EspoCRM create account result: {result}")
    return result
