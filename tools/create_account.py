from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Accounts")
@doc_name("Create Account")
def create_account_tool(
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
    Create a new Account in EspoCRM.

    This tool creates an Account record using common EspoCRM Account fields.
    Parameters map directly to EspoCRM Account attributes. Any parameter set
    to `None` is omitted from the request to avoid sending unnecessary or
    empty values.

    Accounts can include contact details, billing and shipping addresses,
    relationships to campaigns, teams, and target lists, as well as custom
    EspoCRM fields.

    Args:
    - `name` (Optional[str]): Account name (<= 249 characters).
    - `website` (Optional[str]): Website URL (<= 255 characters).
    - `description` (Optional[str]): Description or internal notes.
    - `email_address` (Optional[str]): Primary email address (<= 255 characters).
    - `email_address_data` (Optional[List[Dict[str, Any]]]): Multiple email objects.
    - `email_address_is_opted_out` (Optional[bool]): Email opted-out flag.
    - `email_address_is_invalid` (Optional[bool]): Email invalid flag.
    - `phone_number` (Optional[str]): Primary phone number (<= 36 characters).
    - `phone_number_data` (Optional[List[Dict[str, Any]]]): Multiple phone objects.
    - `phone_number_is_opted_out` (Optional[bool]): Phone opted-out flag.
    - `phone_number_is_invalid` (Optional[bool]): Phone invalid flag.
    - `type` (Optional[str]): Account category (Customer, Investor, Partner, Reseller).
    - `industry` (Optional[str]): Industry (EspoCRM allowed values).
    - `sic_code` (Optional[str]): SIC code (<= 40 characters).
    - `billing_address_street` (Optional[str]): Billing street address.
    - `billing_address_city` (Optional[str]): Billing city.
    - `billing_address_state` (Optional[str]): Billing state.
    - `billing_address_country` (Optional[str]): Billing country.
    - `billing_address_postal_code` (Optional[str]): Billing postal code.
    - `shipping_address_street` (Optional[str]): Shipping street address.
    - `shipping_address_city` (Optional[str]): Shipping city.
    - `shipping_address_state` (Optional[str]): Shipping state.
    - `shipping_address_country` (Optional[str]): Shipping country.
    - `shipping_address_postal_code` (Optional[str]): Shipping postal code.
    - `campaign_id` (Optional[str]): Related Campaign record ID.
    - `assigned_user_id` (Optional[str]): Assigned user ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `target_lists_ids` (Optional[List[str]]): Target List IDs.
    - `target_list_id` (Optional[str]): Target List ID.
    - `email_address_is_opted_out_flag` (Optional[bool]): Maps to `emailAddressIsOptedOut`.
    - `email_address_is_invalid_flag` (Optional[bool]): Maps to `emailAddressIsInvalid`.
    - `phone_number_is_opted_out_flag` (Optional[bool]): Maps to `phoneNumberIsOptedOut`.
    - `phone_number_is_invalid_flag` (Optional[bool]): Maps to `phoneNumberIsInvalid`.
    - `duplicate_source_id` (Optional[str]): Record ID being duplicated (sent as header `X-Duplicate-Source-Id`).
    - `skip_duplicate_check` (Optional[bool]): Skip duplicate check (sent as header `X-Skip-Duplicate-Check`).
    - `custom_fields` (Optional[Dict[str, Any]]): Custom EspoCRM fields (must start with `c` prefix).

    Example Requests:
    - Create a basic account:
      create_account_tool(name="Acme Corp", website="https://acme.com", email_address="info@acme.com")
    - Create an account with multiple emails and phones:
      create_account_tool(name="Acme Corp", email_address_data=[{"emailAddress": "info@acme.com", "primary": True}], phone_number_data=[{"phoneNumber": "+123456789", "type": "Office", "primary": True}])
    - Create an account with addresses and relations:
      create_account_tool(name="Acme Corp", billing_address_city="Bangkok", shipping_address_country="Thailand", assigned_user_id="USER_ID_123")
    - Create an account with custom fields:
      create_account_tool(name="Acme Corp", custom_fields={"c_customer_score": 95, "c_region": "APAC"})

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
