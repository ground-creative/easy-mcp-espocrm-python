from typing import Dict, Any, Optional, List, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("TargetLists")
@doc_name("Create TargetList")
def create_target_list_tool(
    name: Annotated[
        str, Field(description="Name of the TargetList (<=255 chars)")
    ] = None,
    category_id: Annotated[
        Optional[str], Field(description="ID of TargetListCategory")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Description / notes")
    ] = None,
    source_campaign_id: Annotated[
        Optional[str], Field(description="Campaign ID")
    ] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned user ID")
    ] = None,
    teams_ids: Annotated[Optional[List[str]], Field(description="Team IDs")] = None,
    duplicate_source_id: Annotated[
        Optional[str], Field(description="Duplicate source ID")
    ] = None,
    skip_duplicate_check: Annotated[
        Optional[bool], Field(description="Skip duplicate check")
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]], Field(description="Custom fields starting with 'c'")
    ] = None,
) -> Dict:
    """
    Create a new TargetList in EspoCRM.

    Args:
    - `name` (str): TargetList name.
    - `category_id` (Optional[str]): TargetListCategory ID.
    - `description` (Optional[str]): Description text.
    - `source_campaign_id` (Optional[str]): Source Campaign ID.
    - `assigned_user_id` (Optional[str]): Assigned User ID.
    - `teams_ids` (Optional[List[str]]): Team IDs.
    - `duplicate_source_id` (Optional[str]): Record ID of an entity being duplicated.
    - `skip_duplicate_check` (Optional[bool]): Skip duplicate check.
    - `custom_fields` (Optional[Dict[str, Any]]): EspoCRM custom fields prefixed with 'c'.

    Example Requests:
    - Create a simple TargetList:
    `create_target_list_tool(name="Prospects 2026")`
    - Create a TargetList with a category and assigned user:
    `create_target_list_tool(name="Campaign Leads", category_id="cat123", assigned_user_id="user456")`
    - Create a TargetList with custom fields:
    `create_target_list_tool(name="Demo List", custom_fields={"c_priority": "High"})`

    Returns:
    - A structured dict containing the API response with keys:
    `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to create TargetList with params: {locals()}")

    # Check API key and access
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
        "TargetList",
        params=params,
        extra_headers=extra_headers if extra_headers else None,
    )
    logger.debug(f"EspoCRM create TargetList result: {result}")
    return result
