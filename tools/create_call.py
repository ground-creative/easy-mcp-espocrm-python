from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Calls")
@doc_name("Create Call")
def create_call_tool(
    name: Annotated[
        Optional[str], Field(description="A one-line string. <= 255 characters")
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Call status (Planned, Held, Not Held)."),
    ] = None,
    date_start: Annotated[
        Optional[str],
        Field(
            description="A timestamp in UTC. Format: YYYY-MM-DD HH:MM:SS",
        ),
    ] = None,
    date_end: Annotated[
        Optional[str],
        Field(
            description="A timestamp in UTC. Format: YYYY-MM-DD HH:MM:SS",
        ),
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
    parent_name: Annotated[
        Optional[str], Field(description="A foreign record name.")
    ] = None,
    account_id: Annotated[
        Optional[str], Field(description="Account record ID.")
    ] = None,
    account_name: Annotated[Optional[str], Field(description="Account name.")] = None,
    uid: Annotated[
        Optional[str], Field(description="A one-line string. <= 255 characters")
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
    Create a new Call in EspoCRM.

    This tool creates a Call record using common Call fields. Parameters map directly
    to EspoCRM Call attributes. Any parameter set to `None` is omitted from the request
    to avoid overwriting default values.

    Calls can be linked to other entities such as Accounts, Leads, Contacts, or Opportunities,
    and can include multiple participants via users, contacts, or leads relationships.

    Args:
    - `name` (Optional[str]): Call subject or title (<= 255 chars).
    - `status` (Optional[str]): Call status. Allowed values: Planned, Held, Not Held.
    - `date_start` (Optional[str]): Call start time in UTC (YYYY-MM-DD HH:MM:SS).
    - `date_end` (Optional[str]): Call end time in UTC (YYYY-MM-DD HH:MM:SS).
    - `direction` (Optional[str]): Call direction. Allowed values: Outbound, Inbound.
    - `description` (Optional[str]): Multi-line description or notes.
    - `parent_id` (Optional[str]): ID of the related parent record.
    - `parent_type` (Optional[str]): Parent entity type (Account, Lead, Contact, Opportunity, Case, CCompany).
    - `parent_name` (Optional[str]): Name of the related parent record.
    - `account_id` (Optional[str]): Related Account record ID.
    - `account_name` (Optional[str]): Related Account name.
    - `uid` (Optional[str]): External unique identifier (<= 255 chars).
    - `acceptance_status` (Optional[str]): Acceptance status (None, Accepted, Tentative, Declined).
    - `users_ids` (Optional[List[str]]): IDs of User participants.
    - `users_columns` (Optional[Dict[str, Any]]): Relationship column values for users.
    - `users_names` (Optional[Dict[str, str]]): User ID to name mapping.
    - `contacts_ids` (Optional[List[str]]): IDs of Contact participants.
    - `contacts_columns` (Optional[Dict[str, Any]]): Relationship column values for contacts.
    - `contacts_names` (Optional[Dict[str, str]]): Contact ID to name mapping.
    - `leads_ids` (Optional[List[str]]): IDs of Lead participants.
    - `leads_columns` (Optional[Dict[str, Any]]): Relationship column values for leads.
    - `leads_names` (Optional[Dict[str, str]]): Lead ID to name mapping.
    - `assigned_user_id` (Optional[str]): Assigned user ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `duplicate_source_id` (Optional[str]): Record ID being duplicated (sent as header `X-Duplicate-Source-Id`).
    - `skip_duplicate_check` (Optional[bool]): Skip duplicate check (sent as header `X-Skip-Duplicate-Check`).
    - `custom_fields` (Optional[Dict[str, Any]]): Custom EspoCRM fields (must start with `c` prefix).

    Example Requests:
    - Create a basic planned outbound call:
      create_call_tool(name="Intro Call", status="Planned", direction="Outbound", date_start="2026-01-01 10:00:00")
    - Create a held call linked to a Lead:
      create_call_tool(name="Follow-up Call", status="Held", parent_type="Lead", parent_id="LEAD_ID_123")
    - Create a call with multiple participants:
      create_call_tool(name="Sales Call", users_ids=["USER_ID_1"], contacts_ids=["CONTACT_ID_1"])
    - Create a call with custom fields:
      create_call_tool(name="Demo Call", custom_fields={"c_call_score": 95, "c_recording_url": "https://example.com/recording"})

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to create call with params: {locals()}")

    # Check api key and address are set in headers
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Exclude header-only params from request body
    params = build_espo_params(
        locals(),
        exclude={"duplicate_source_id", "skip_duplicate_check", "auth_response"},
    )

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

    result = client.call_api(
        "POST",
        "Call",
        params=params,
        extra_headers=extra_headers if extra_headers else None,
    )
    logger.debug(f"EspoCRM create call result: {result}")
    return result
