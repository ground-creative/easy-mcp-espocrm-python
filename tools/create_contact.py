from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Contacts")
@doc_name("Create Contact")
def create_contact_tool(
    salutation_name: Annotated[
        Optional[str], Field(description="Salutation (Mr., Ms., Dr., etc.)")
    ] = None,
    first_name: Annotated[
        Optional[str], Field(description="First name (<=100 chars)")
    ] = None,
    middle_name: Annotated[
        Optional[str], Field(description="Middle name (<=100 chars)")
    ] = None,
    last_name: Annotated[
        Optional[str], Field(description="Last name (<=100 chars)")
    ] = None,
    title: Annotated[Optional[str], Field(description="Title (<=100 chars)")] = None,
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
    phone_number: Annotated[
        Optional[str], Field(description="Primary phone number (<=36 chars)")
    ] = None,
    phone_number_data: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Multiple phone numbers array of objects"),
    ] = None,
    do_not_call: Annotated[
        Optional[bool], Field(description="Do not call flag")
    ] = None,
    address_street: Annotated[
        Optional[str], Field(description="Street (<=255 chars)")
    ] = None,
    address_city: Annotated[
        Optional[str], Field(description="City (<=100 chars)")
    ] = None,
    address_state: Annotated[
        Optional[str], Field(description="State (<=100 chars)")
    ] = None,
    address_country: Annotated[
        Optional[str], Field(description="Country (<=100 chars)")
    ] = None,
    address_postal_code: Annotated[
        Optional[str], Field(description="Postal code (<=40 chars)")
    ] = None,
    account_id: Annotated[
        Optional[str], Field(description="ID of related Account")
    ] = None,
    accounts_ids: Annotated[
        Optional[List[str]], Field(description="IDs of related Accounts")
    ] = None,
    account_role: Annotated[Optional[str], Field(description="Account role")] = None,
    opportunity_role: Annotated[
        Optional[str], Field(description="Opportunity role")
    ] = None,
    campaign_id: Annotated[Optional[str], Field(description="Campaign ID")] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned user ID")
    ] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
    target_list_id: Annotated[
        Optional[str], Field(description="Target list ID")
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
    duplicate_source_id: Annotated[
        Optional[str],
        Field(
            description="Record ID of entity being duplicated. Sent as header 'X-Duplicate-Source-Id'."
        ),
    ] = None,
    skip_duplicate_check: Annotated[
        Optional[bool],
        Field(
            description="Skip duplicate check. Sent as header 'X-Skip-Duplicate-Check'."
        ),
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(description="Custom EspoCRM fields, must start with `c` prefix"),
    ] = None,
) -> Dict:
    """
    Create a new Contact in EspoCRM.

    This tool creates a Contact record using common Contact fields. Any parameter set to `None` is omitted from the request to avoid overwriting defaults. Supports optional headers for duplicate handling.

    Args:
    - `salutation_name` (Optional[str]): Salutation (Mr., Ms., Mrs., Dr., etc.).
    - `first_name` (Optional[str]): First name (<=100 chars).
    - `middle_name` (Optional[str]): Middle name (<=100 chars).
    - `last_name` (Optional[str]): Last name (<=100 chars).
    - `title` (Optional[str]): Job title (<=100 chars).
    - `description` (Optional[str]): Multi-line description or notes.
    - `email_address` (Optional[str]): Primary email (<=255 chars).
    - `email_address_data` (Optional[List[Dict[str, Any]]]): Multiple email objects. Each object: `emailAddress` (str, required), `primary` (bool, required), `optOut` (bool, optional), `invalid` (bool, optional)
    - `phone_number` (Optional[str]): Primary phone number (<=36 chars).
    - `phone_number_data` (Optional[List[Dict[str, Any]]]): Multiple phone objects. Each object: `phoneNumber` (str, required), `primary` (bool, required), `optOut` (bool, optional), `invalid` (bool, optional)
    - `do_not_call` (Optional[bool]): Do not call flag.
    - `address_street` (Optional[str]): Street address (<=255 chars).
    - `address_city` (Optional[str]): City (<=100 chars).
    - `address_state` (Optional[str]): State (<=100 chars).
    - `address_country` (Optional[str]): Country (<=100 chars).
    - `address_postal_code` (Optional[str]): Postal code (<=40 chars).
    - `account_id` (Optional[str]): Related Account ID.
    - `accounts_ids` (Optional[List[str]]): Multiple related Account IDs.
    - `accounts_columns` (Optional[Dict[str, Dict[str, Any]]]): {AccountID => column values} for relationships.
    - `account_role` (Optional[str]): Account role.
    - `account_is_inactive` (Optional[bool]): Account inactive flag.
    - `opportunity_role` (Optional[str]): Opportunity role (Decision Maker, Evaluator, Influencer).
    - `campaign_id` (Optional[str]): Related Campaign ID.
    - `assigned_user_id` (Optional[str]): Assigned User ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `target_list_id` (Optional[str]): Target List ID.
    - `original_lead_id` (Optional[str]): Original Lead ID if created from a Lead.
    - `original_email_id` (Optional[str]): Original Email ID.
    - `email_address_is_opted_out` (Optional[bool]): Email opted out flag.
    - `email_address_is_invalid` (Optional[bool]): Email invalid flag.
    - `phone_number_is_opted_out` (Optional[bool]): Phone opted out flag.
    - `phone_number_is_invalid` (Optional[bool]): Phone invalid flag.
    - `duplicate_source_id` (Optional[str]): Record ID of entity being duplicated, sent as header `X-Duplicate-Source-Id`.
    - `skip_duplicate_check` (Optional[bool]): Skip duplicate check, sent as header `X-Skip-Duplicate-Check` with value 'true' or 'false'.
    - `custom_fields` (Optional[Dict[str, Any]]): Custom EspoCRM fields prefixed with c.

    Example Requests:
    - Create a basic contact: create_contact_tool(first_name="Jane", last_name="Doe", email_address="jane@example.com")
    - Create a contact with multiple emails and phones: create_contact_tool(first_name="Acme", last_name="Inc", email_address_data=[{"emailAddress": "a@acme.com", "primary": True}], phone_number_data=[{"phoneNumber": "+123456789", "primary": True}])
    - Create a contact with custom fields: create_contact_tool(first_name="Demo", last_name="User", custom_fields={"c_demo_field": "value"})

    Returns:
    - A structured dict containing the API response with keys: `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to create contact with params: {locals()}")

    # Check API key
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Build params, exclude headers
    params = build_espo_params(
        locals(),
        exclude={"duplicate_source_id", "skip_duplicate_check", "auth_response"},
    )

    # Build headers for duplicate handling
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

    # POST request to create Contact
    result = client.call_api(
        "POST",
        "Contact",
        params=params,
        extra_headers=extra_headers if extra_headers else None,
    )
    logger.debug(f"EspoCRM create contact result: {result}")
    return result
