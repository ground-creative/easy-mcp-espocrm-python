from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Campaigns")
@doc_name("Create Campaign")
def espo_create_campaign_tool(
    name: Annotated[str, Field(description="Campaign name (<= 255 chars)")],
    status: Annotated[Optional[str], Field(description="Campaign status (Planning, Active, Inactive, Complete)")] = None,
    type: Annotated[Optional[str], Field(description="Campaign type (Email, Newsletter, Informational Email, Web, Television, Radio, Mail)")] = None,
    start_date: Annotated[Optional[str], Field(description="Start date (YYYY-MM-DD)")] = None,
    end_date: Annotated[Optional[str], Field(description="End date (YYYY-MM-DD)")] = None,
    description: Annotated[Optional[str], Field(description="Multi-line description")] = None,
    assigned_user_id: Annotated[Optional[str], Field(description="Assigned user ID")] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
    target_lists_ids: Annotated[Optional[List[str]], Field(description="Target List IDs")] = None,
    excluding_target_lists_ids: Annotated[Optional[List[str]], Field(description="Excluded Target List IDs")] = None,
    budget: Annotated[Optional[float], Field(description="Budget amount")] = None,
    budget_currency: Annotated[Optional[str], Field(description="Currency code (USD, EUR)")] = None,
    contacts_template_id: Annotated[Optional[str], Field(description="Template ID for contacts")] = None,
    leads_template_id: Annotated[Optional[str], Field(description="Template ID for leads")] = None,
    accounts_template_id: Annotated[Optional[str], Field(description="Template ID for accounts")] = None,
    users_template_id: Annotated[Optional[str], Field(description="Template ID for users")] = None,
    mail_merge_only_with_address: Annotated[Optional[bool], Field(description="Mail merge only with address flag")] = None,
    duplicate_source_id: Annotated[Optional[str], Field(description="Record ID being duplicated. Sent as header 'X-Duplicate-Source-Id'.")] = None,
    skip_duplicate_check: Annotated[Optional[bool], Field(description="Skip duplicate check. Sent as header 'X-Skip-Duplicate-Check' with 'true' or 'false'.")] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(description="Custom EspoCRM fields (must start with 'c', e.g., cSomeCustomField)")
    ] = None,
) -> Dict:
    """
    Create a new Campaign in EspoCRM.

    This tool creates a Campaign record using common Campaign fields. Any parameter set to `None` is omitted
    from the request to avoid overwriting defaults. Supports optional headers for duplicate handling.

    Args:
    - `name` (str): Campaign name (<= 255 chars).
    - `status` (Optional[str]): Campaign status (Planning, Active, Inactive, Complete).
    - `type` (Optional[str]): Campaign type (Email, Newsletter, Informational Email, Web, Television, Radio, Mail).
    - `start_date` (Optional[str]): Start date (YYYY-MM-DD).
    - `end_date` (Optional[str]): End date (YYYY-MM-DD).
    - `description` (Optional[str]): Multi-line description.
    - `assigned_user_id` (Optional[str]): Assigned user ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `target_lists_ids` (Optional[List[str]]): Target List IDs.
    - `excluding_target_lists_ids` (Optional[List[str]]): Excluded Target List IDs.
    - `budget` (Optional[float]): Budget amount.
    - `budget_currency` (Optional[str]): Currency code (USD, EUR).
    - `contacts_template_id` (Optional[str]): Template ID for contacts.
    - `leads_template_id` (Optional[str]): Template ID for leads.
    - `accounts_template_id` (Optional[str]): Template ID for accounts.
    - `users_template_id` (Optional[str]): Template ID for users.
    - `mail_merge_only_with_address` (Optional[bool]): Mail merge only with address flag.
    - `duplicate_source_id` (Optional[str]): Record ID of entity being duplicated, sent as header `X-Duplicate-Source-Id`.
    - `skip_duplicate_check` (Optional[bool]): Skip duplicate check flag. Sent as header `X-Skip-Duplicate-Check` with value `'true'` or `'false'`.
    - `custom_fields` (Optional[Dict[str, Any]]): Custom EspoCRM fields prefixed with `c`.

    Example Requests:
    - Create a basic campaign:
      espo_create_campaign_tool(name="Summer Sale 2026", status="Planning", type="Email")
    - Create a campaign with assigned user, teams, and budget:
      espo_create_campaign_tool(name="Product Launch", status="Active", type="Web", assigned_user_id="abc123", teams_ids=["team1", "team2"], budget=5000, budget_currency="USD")
    - Create a campaign with custom fields:
      espo_create_campaign_tool(name="Demo Campaign", type="Email", custom_fields={"c_customCode": "XYZ", "c_priority": 1})

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to create campaign with params: {locals()}")

    # Check api key and address
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Exclude header-only params from request body
    params = build_espo_params(
        locals(), exclude={"duplicate_source_id", "skip_duplicate_check", "auth_response"}
    )

    # Build headers for duplicate handling if provided
    extra_headers = {}
    if duplicate_source_id:
        extra_headers["X-Duplicate-Source-Id"] = str(duplicate_source_id)
    if skip_duplicate_check is not None:
        extra_headers["X-Skip-Duplicate-Check"] = "true" if skip_duplicate_check else "false"

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Call API
    result = client.call_api(
        'POST', 'Campaign', params=params, extra_headers=extra_headers if extra_headers else None
    )
    logger.debug(f"EspoCRM create campaign result: {result}")
    return result
