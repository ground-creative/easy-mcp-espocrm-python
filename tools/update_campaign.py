from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Campaigns")
@doc_name("Update Campaign")
def update_campaign_tool(
    campaign_id: str,
    name: Annotated[
        Optional[str], Field(description="Campaign name (<=255 chars)")
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Campaign status (Planning, Active, Inactive, Complete)"),
    ] = None,
    type: Annotated[
        Optional[str],
        Field(
            description="Campaign type (Email, Newsletter, Informational Email, Web, Television, Radio, Mail)"
        ),
    ] = None,
    start_date: Annotated[
        Optional[str], Field(description="Start date (YYYY-MM-DD)")
    ] = None,
    end_date: Annotated[
        Optional[str], Field(description="End date (YYYY-MM-DD)")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Multi-line description")
    ] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned user ID")
    ] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
    target_lists_ids: Annotated[
        Optional[List[str]], Field(description="Target List IDs")
    ] = None,
    excluding_target_lists_ids: Annotated[
        Optional[List[str]], Field(description="Excluded Target List IDs")
    ] = None,
    budget: Annotated[Optional[float], Field(description="Budget amount")] = None,
    budget_currency: Annotated[
        Optional[str], Field(description="Budget currency code (USD, EUR)")
    ] = None,
    contacts_template_id: Annotated[
        Optional[str], Field(description="Template ID for contacts")
    ] = None,
    leads_template_id: Annotated[
        Optional[str], Field(description="Template ID for leads")
    ] = None,
    accounts_template_id: Annotated[
        Optional[str], Field(description="Template ID for accounts")
    ] = None,
    users_template_id: Annotated[
        Optional[str], Field(description="Template ID for users")
    ] = None,
    mail_merge_only_with_address: Annotated[
        Optional[bool], Field(description="Mail merge only with address flag")
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(
            description="Custom EspoCRM fields (must start with 'c', e.g., cSomeCustomField)"
        ),
    ] = None,
) -> Dict:
    """
    Update an existing Campaign in EspoCRM.

    This tool updates a Campaign record by `campaign_id`. Provide any Campaign fields to update.
    Parameters left as `None` will not be sent to avoid overwriting unchanged values.

    Args:
    - `campaign_id` (str): ID of the Campaign record to update.
    - `name` (Optional[str]): Campaign name (<=255 chars).
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
    - `budget_currency` (Optional[str]): Budget currency code (USD, EUR).
    - `contacts_template_id` (Optional[str]): Template ID for contacts.
    - `leads_template_id` (Optional[str]): Template ID for leads.
    - `accounts_template_id` (Optional[str]): Template ID for accounts.
    - `users_template_id` (Optional[str]): Template ID for users.
    - `mail_merge_only_with_address` (Optional[bool]): Mail merge only with address flag.
    - `custom_fields` (Optional[Dict[str, Any]]): A dictionary of EspoCRM custom fields to update on the Campaign record. All EspoCRM custom fields are prefixed with `c`.

    Example Requests:
    - Update campaign name and status:
      update_campaign_tool(campaign_id="abc123", name="Spring Promo", status="Active")
    - Update campaign teams and budget:
      update_campaign_tool(campaign_id="abc123", teams_ids=["team1","team2"], budget=10000, budget_currency="USD")
    - Update custom fields on a campaign:
      update_campaign_tool(campaign_id="abc123", custom_fields={"c_campaign_code":"X123","c_priority":2})

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(
        f"Request received to update campaign {campaign_id} with params: {locals()}"
    )

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Build params excluding path/id and internal vars
    params = build_espo_params(locals(), exclude={"campaign_id", "auth_response"})

    # Merge custom fields if provided
    if custom_fields:
        params.update(custom_fields)

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Call EspoCRM PATCH endpoint for the campaign
    result = client.call_api("PATCH", f"Campaign/{campaign_id}", params=params)
    logger.debug(f"EspoCRM update campaign result: {result}")
    return result
