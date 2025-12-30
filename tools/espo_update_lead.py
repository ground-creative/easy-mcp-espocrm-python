from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag


@doc_tag("Leads")
def espo_update_lead_tool(
    lead_id: str,
    salutation_name: Annotated[Optional[str], Field(description="Salutation (Mr., Ms., Dr., etc.)")] = None,
    first_name: Annotated[Optional[str], Field(description="First name (<=100 chars)")] = None,
    middle_name: Annotated[Optional[str], Field(description="Middle name (<=100 chars)")] = None,
    last_name: Annotated[Optional[str], Field(description="Last name (<=100 chars)")] = None,
    title: Annotated[Optional[str], Field(description="Title (<=100 chars)")] = None,
    status: Annotated[Optional[str], Field(description="Lead status (New, Assigned, In Process, Converted, Recycled, Dead)")] = None,
    source: Annotated[Optional[str], Field(description="Lead source (Call, Email, Campaign, etc.)")] = None,
    industry: Annotated[Optional[str], Field(description="Industry (see allowed values)")] = None,
    opportunity_amount: Annotated[Optional[float], Field(description="Opportunity amount (>=0)")] = None,
    opportunity_amount_currency: Annotated[Optional[str], Field(description="Currency code (USD, EUR)")] = None,
    website: Annotated[Optional[str], Field(description="Website (<=255 chars)")] = None,
    address_street: Annotated[Optional[str], Field(description="Street (<=255 chars)")] = None,
    address_city: Annotated[Optional[str], Field(description="City (<=100 chars)")] = None,
    address_state: Annotated[Optional[str], Field(description="State (<=100 chars)")] = None,
    address_country: Annotated[Optional[str], Field(description="Country (<=100 chars)")] = None,
    address_postal_code: Annotated[Optional[str], Field(description="Postal code (<=40 chars)")] = None,
    email_address: Annotated[Optional[str], Field(description="Primary email (<=255 chars)")] = None,
    email_address_data: Annotated[Optional[List[Dict[str, Any]]], Field(description="Multiple emails array of objects")]= None,
    phone_number: Annotated[Optional[str], Field(description="Primary phone number (<=36 chars)")] = None,
    phone_number_data: Annotated[Optional[List[Dict[str, Any]]], Field(description="Multiple phone numbers array of objects")]= None,
    do_not_call: Annotated[Optional[bool], Field(description="Do not call flag")] = None,
    description: Annotated[Optional[str], Field(description="Description / notes")]= None,
    account_name: Annotated[Optional[str], Field(description="Account name (<=255 chars)")] = None,
    assigned_user_id: Annotated[Optional[str], Field(description="Assigned user ID")]= None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")]= None,
    campaign_id: Annotated[Optional[str], Field(description="Campaign ID")]= None,
    target_list_id: Annotated[Optional[str], Field(description="Target list ID")]= None,
    duplicate_source_id: Annotated[Optional[str], Field(description="Record ID of an entity being duplicated. Sent as header 'X-Duplicate-Source-Id'.")] = None,
    skip_duplicate_check: Annotated[Optional[bool], Field(description="Skip duplicate check. Sent as header 'X-Skip-Duplicate-Check' with value 'true' or 'false'.")] = None,
 ) -> Dict:
    """
    Update an existing Lead in EspoCRM.

    This tool updates a Lead record by `lead_id`. Provide any Lead fields to
    update; parameters left as `None` will not be sent to avoid overwriting
    unchanged values.

    Args:
    - `lead_id` (str): ID of the Lead record to update.
    - `salutation_name` (Optional[str]): Salutation (e.g. 'Mr.', 'Ms.', 'Dr.').
    - `first_name` (Optional[str]): First name (<= 100 chars).
    - `middle_name` (Optional[str]): Middle name (<= 100 chars).
    - `last_name` (Optional[str]): Last name (<= 100 chars).
    - `title` (Optional[str]): Job title (<= 100 chars).
    - `status` (Optional[str]): Lead status (New, Assigned, In Process, Converted, Recycled, Dead).
    - `source` (Optional[str]): Lead source (Call, Email, Campaign, etc.).
    - `industry` (Optional[str]): Industry (see API allowed values).
    - `opportunity_amount` (Optional[float]): Opportunity amount (>= 0).
    - `opportunity_amount_currency` (Optional[str]): Currency code (USD, EUR).
    - `website` (Optional[str]): Website (<= 255 chars).
    - `address_street` (Optional[str]): Street (<= 255 chars).
    - `address_city` (Optional[str]): City (<= 100 chars).
    - `address_state` (Optional[str]): State (<= 100 chars).
    - `address_country` (Optional[str]): Country (<= 100 chars).
    - `address_postal_code` (Optional[str]): Postal code (<= 40 chars).
    - `email_address` (Optional[str]): Primary email (<= 255 chars).
    - `email_address_data` (Optional[List[Dict[str, Any]]]): Multiple email objects.
    - `phone_number` (Optional[str]): Primary phone (<= 36 chars).
    - `phone_number_data` (Optional[List[Dict[str, Any]]]): Multiple phone objects.
    - `do_not_call` (Optional[bool]): Do not call flag.
    - `description` (Optional[str]): Description / notes.
    - `account_name` (Optional[str]): Account name (<= 255 chars).
    - `assigned_user_id` (Optional[str]): ID of the assigned User record.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `campaign_id` (Optional[str]): Campaign ID.
    - `target_list_id` (Optional[str]): Target list ID.
   
    Example Requests:
    - Update a lead's name and email:
      ```python
      espo_update_lead_tool(lead_id="abc123", first_name="Jane", last_name="Doe", email_address="jane@example.com")
      ```
    - Update multiple fields including phone numbers:
      ```python
      espo_update_lead_tool(
          lead_id="abc123",
          phone_number_data=[{"phoneNumber": "+123456789", "primary": True}],
          do_not_call=True
      )
      ```

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to update lead {lead_id} with params: {locals()}")

    # Check api key and address are set in headers
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    params = build_espo_params(locals(), exclude={"lead_id", "auth_response"})
    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api('PATCH', f'Lead/{lead_id}', params=params)
    logger.debug(f"EspoCRM update lead result: {result}")
    return result
