from typing import Dict, Any, Optional, List, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Contacts")
@doc_name("Update Contact")
def espo_update_contact_tool(
    contact_id: Annotated[str, Field(description="The ID of the Contact record to update")],
    salutation_name: Annotated[Optional[str], Field(description="Salutation (Mr., Ms., Dr., etc.)")] = None,
    first_name: Annotated[Optional[str], Field(description="First name (<=100 chars)")] = None,
    middle_name: Annotated[Optional[str], Field(description="Middle name (<=100 chars)")] = None,
    last_name: Annotated[Optional[str], Field(description="Last name (<=100 chars)")] = None,
    title: Annotated[Optional[str], Field(description="Job title (<=100 chars)")] = None,
    description: Annotated[Optional[str], Field(description="Multi-line description / notes")] = None,
    email_address: Annotated[Optional[str], Field(description="Primary email (<=255 chars)")] = None,
    email_address_data: Annotated[Optional[List[Dict[str, Any]]], Field(description="Multiple email objects with keys: emailAddress (str), primary (bool), optOut (bool, optional), invalid (bool, optional)")] = None,
    phone_number: Annotated[Optional[str], Field(description="Primary phone number (<=36 chars)")] = None,
    phone_number_data: Annotated[Optional[List[Dict[str, Any]]], Field(description="Multiple phone objects with keys: phoneNumber (str), primary (bool), optOut (bool, optional), invalid (bool, optional)")] = None,
    do_not_call: Annotated[Optional[bool], Field(description="Do not call flag")] = None,
    address_street: Annotated[Optional[str], Field(description="Street address (<=255 chars)")] = None,
    address_city: Annotated[Optional[str], Field(description="City (<=100 chars)")] = None,
    address_state: Annotated[Optional[str], Field(description="State (<=100 chars)")] = None,
    address_country: Annotated[Optional[str], Field(description="Country (<=100 chars)")] = None,
    address_postal_code: Annotated[Optional[str], Field(description="Postal code (<=40 chars)")] = None,
    account_id: Annotated[Optional[str], Field(description="Related Account ID")] = None,
    accounts_ids: Annotated[Optional[List[str]], Field(description="Multiple related Account IDs")] = None,
    accounts_columns: Annotated[Optional[Dict[str, Any]], Field(description="AccountID => column values mapping for relationships")] = None,
    account_role: Annotated[Optional[str], Field(description="Account role")] = None,
    account_is_inactive: Annotated[Optional[bool], Field(description="Account inactive flag")] = None,
    opportunity_role: Annotated[Optional[str], Field(description="Opportunity role (Decision Maker, Evaluator, Influencer)")] = None,
    campaign_id: Annotated[Optional[str], Field(description="Related Campaign ID")] = None,
    assigned_user_id: Annotated[Optional[str], Field(description="Assigned user ID")] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
    target_list_id: Annotated[Optional[str], Field(description="Target List ID")] = None,
    target_lists_ids: Annotated[Optional[List[str]], Field(description="Multiple Target List IDs")] = None,
    original_email_id: Annotated[Optional[str], Field(description="Original Email ID")] = None,
    email_address_is_opted_out: Annotated[Optional[bool], Field(description="Email opted out flag")] = None,
    email_address_is_invalid: Annotated[Optional[bool], Field(description="Email invalid flag")] = None,
    phone_number_is_opted_out: Annotated[Optional[bool], Field(description="Phone opted out flag")] = None,
    phone_number_is_invalid: Annotated[Optional[bool], Field(description="Phone invalid flag")] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(description="Custom EspoCRM fields (must start with `c` prefix, e.g., cCustomField)")
    ] = None,
) -> Dict:
    """
    Update an existing Contact in EspoCRM.

    This tool updates a Contact record using standard Contact fields. Any parameter set to `None` is omitted
    from the request to avoid overwriting existing data.

    Args:
    - `contact_id` (str): The ID of the Contact record.
    - `salutation_name` (Optional[str]): Salutation (Mr., Ms., Mrs., Dr., etc.).
    - `first_name` (Optional[str]): First name (<=100 chars).
    - `middle_name` (Optional[str]): Middle name (<=100 chars).
    - `last_name` (Optional[str]): Last name (<=100 chars).
    - `title` (Optional[str]): Job title (<=100 chars).
    - `description` (Optional[str]): Multi-line description.
    - `email_address` (Optional[str]): Primary email (<=255 chars).
    - `email_address_data` (Optional[List[Dict[str, Any]]]): Multiple email objects.
    - `phone_number` (Optional[str]): Primary phone (<=36 chars).
    - `phone_number_data` (Optional[List[Dict[str, Any]]]): Multiple phone objects.
    - `do_not_call` (Optional[bool]): Do not call flag.
    - `address_street` (Optional[str]): Street address (<=255 chars).
    - `address_city` (Optional[str]): City (<=100 chars).
    - `address_state` (Optional[str]): State (<=100 chars).
    - `address_country` (Optional[str]): Country (<=100 chars).
    - `address_postal_code` (Optional[str]): Postal code (<=40 chars).
    - `account_id` (Optional[str]): Related Account ID.
    - `accounts_ids` (Optional[List[str]]): Multiple related Account IDs.
    - `accounts_columns` (Optional[Dict[str, Any]]): {AccountID => column values} for relationships.
    - `account_role` (Optional[str]): Account role.
    - `account_is_inactive` (Optional[bool]): Account inactive flag.
    - `opportunity_role` (Optional[str]): Opportunity role (Decision Maker, Evaluator, Influencer).
    - `campaign_id` (Optional[str]): Related Campaign ID.
    - `assigned_user_id` (Optional[str]): Assigned User ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `target_lists_ids` (Optional[List[str]]): Target List IDs.
    - `target_list_id` (Optional[str]): Target List ID.
    - `original_email_id` (Optional[str]): Original Email ID.
    - `email_address_is_opted_out` (Optional[bool]): Email opted out flag.
    - `email_address_is_invalid` (Optional[bool]): Email invalid flag.
    - `phone_number_is_opted_out` (Optional[bool]): Phone opted out flag.
    - `phone_number_is_invalid` (Optional[bool]): Phone invalid flag.
    - `custom_fields` (Optional[Dict[str, Any]]): A dictionary of EspoCRM custom fields to update on the Lead record. All EspoCRM custom fields are prefixed with `c`.

    Example Requests:
    - Update a contact's name: espo_update_contact_tool(contact_id="abc123", first_name="John", last_name="Doe")
    - Update emails and phones: espo_update_contact_tool(contact_id="abc123", email_address_data=[{"emailAddress":"a@acme.com","primary":True}], phone_number_data=[{"phoneNumber":"+123456789","primary":True}])
    - Update address: espo_update_contact_tool(contact_id="abc123", address_street="123 Main St", address_city="Bangkok", address_country="Thailand")

    Returns:
    - A structured dict containing the API response with keys: `status_code`, `ok`, `data`, `error`, `error_type`.
      The `data` object contains updated Contact fields similar to Read Contact.
    """
    logger.info(f"Request received to update Contact with id: {contact_id}")

    # Check api key and address are set in headers
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    params = build_espo_params(locals(), exclude={"contact_id", "auth_response"})

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)
    result = client.call_api('PATCH', f'Contact/{contact_id}', params=params)
    logger.debug(f"EspoCRM update contact result: {result}")
    return result
