from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Calls")
@doc_name("Update Call")
def update_call_tool(
    call_id: str,
    name: Annotated[
        Optional[str], Field(description="A one-line string. <= 255 characters")
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Call status (Planned, Held, Not Held)."),
    ] = None,
    date_start: Annotated[
        Optional[str],
        Field(description="A timestamp in UTC. Format: YYYY-MM-DD HH:MM:SS"),
    ] = None,
    date_end: Annotated[
        Optional[str],
        Field(description="A timestamp in UTC. Format: YYYY-MM-DD HH:MM:SS"),
    ] = None,
    direction: Annotated[
        Optional[str], Field(description="Direction: Outbound or Inbound")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="A multi-line text.")
    ] = None,
    parent_id: Annotated[
        Optional[str], Field(description="A foreign record ID.")
    ] = None,
    parent_type: Annotated[
        Optional[str],
        Field(
            description=(
                "An entity type. Allowed: Account, Lead, Contact, Opportunity, Case, CCompany"
            )
        ),
    ] = None,
    acceptance_status: Annotated[
        Optional[str],
        Field(description="Acceptance status (None, Accepted, Tentative, Declined)"),
    ] = None,
    users_ids: Annotated[
        Optional[List[str]], Field(description="IDs of User records.")
    ] = None,
    users_columns: Annotated[
        Optional[Dict[str, Any]],
        Field(description="{ID => object} map for relationship columns"),
    ] = None,
    users_names: Annotated[
        Optional[Dict[str, str]], Field(description="{ID => name} map for users")
    ] = None,
    contacts_ids: Annotated[
        Optional[List[str]], Field(description="IDs of Contact records.")
    ] = None,
    contacts_columns: Annotated[
        Optional[Dict[str, Any]],
        Field(description="{ID => object} map for relationship columns"),
    ] = None,
    contacts_names: Annotated[
        Optional[Dict[str, str]], Field(description="{ID => name} map for contacts")
    ] = None,
    leads_ids: Annotated[
        Optional[List[str]], Field(description="IDs of Lead records.")
    ] = None,
    leads_columns: Annotated[
        Optional[Dict[str, Any]],
        Field(description="{ID => object} map for relationship columns"),
    ] = None,
    leads_names: Annotated[
        Optional[Dict[str, str]], Field(description="{ID => name} map for leads")
    ] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned user ID")
    ] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
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
        Field(
            description="Custom EspoCRM fields (prefix with `c` e.g. cSomeCustomField)."
        ),
    ] = None,
) -> Dict:
    """
    Update an existing Call in EspoCRM.

    This tool updates a Call record by `call_id`. Provide any Call fields to update.
    Parameters left as `None` will not be sent to avoid overwriting unchanged values.

    Args:
    - `call_id` (str): ID of the Call record to update.
    - `name` (Optional[str]): Call subject or title (<= 255 chars).
    - `status` (Optional[str]): Call status. Allowed values: Planned, Held, Not Held.
    - `date_start` (Optional[str]): Call start time in UTC (YYYY-MM-DD HH:MM:SS).
    - `date_end` (Optional[str]): Call end time in UTC (YYYY-MM-DD HH:MM:SS).
    - `direction` (Optional[str]): Call direction. Allowed values: Outbound, Inbound.
    - `description` (Optional[str]): Multi-line description or notes.
    - `parent_id` (Optional[str]): ID of the related parent record.
    - `parent_type` (Optional[str]): Parent entity type (Account, Lead, Contact, Opportunity, Case, CCompany).
    - `acceptance_status` (Optional[str]): Acceptance status (None, Accepted, Tentative, Declined).
    - `users_ids` / `users_columns` / `users_names`: Participants (users) relationship maps.
    - `contacts_ids` / `contacts_columns` / `contacts_names`: Participants (contacts) relationship maps.
    - `leads_ids` / `leads_columns` / `leads_names`: Participants (leads) relationship maps.
    - `assigned_user_id` (Optional[str]): Assigned user ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `duplicate_source_id` (Optional[str]): Record ID being duplicated (sent as header `X-Duplicate-Source-Id`).
    - `skip_duplicate_check` (Optional[bool]): Skip duplicate check (sent as header `X-Skip-Duplicate-Check`).
    - `custom_fields` (Optional[Dict[str, Any]]): Custom EspoCRM fields to update on the Call record. Custom fields must start with `c` prefix.

    Example Requests:
    - Update call name and start time:
      update_call_tool(call_id="abc123", name="Rescheduled Call", date_start="2026-02-01 09:00:00")
    - Update participants and direction:
      update_call_tool(call_id="abc123", users_ids=["USER1","USER2"], contacts_ids=["CONTACT1"], direction="Inbound")
    - Update custom fields:
      update_call_tool(call_id="abc123", custom_fields={"c_priority": "high", "c_score": 75})

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to update call {call_id} with params: {locals()}")

    # Check API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    params = build_espo_params(locals(), exclude={"call_id", "auth_response"})

    if custom_fields:
        params.update(custom_fields)

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api("PATCH", f"Call/{call_id}", params=params)
    logger.debug(f"EspoCRM update call result: {result}")
    return result
