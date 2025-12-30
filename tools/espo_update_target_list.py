from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("TargetLists")
@doc_name("Update TargetList")
def espo_update_target_list_tool(
    target_list_id: str,
    name: Annotated[
        Optional[str], Field(description="TargetList name (<=255 chars)")
    ] = None,
    category_id: Annotated[
        Optional[str], Field(description="TargetListCategory ID")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Description / notes")
    ] = None,
    source_campaign_id: Annotated[
        Optional[str], Field(description="Source campaign ID")
    ] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned User ID")
    ] = None,
    teams_ids: Annotated[
        Optional[List[str]], Field(description="List of Team IDs")
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(
            description="Custom EspoCRM fields starting with 'c', e.g., cCustomField"
        ),
    ] = None,
) -> Dict:
    """
    Update an existing TargetList record in EspoCRM.

    Args:
    - `target_list_id` (str): ID of the TargetList record to update.
    - `name` (Optional[str]): Name of the TargetList.
    - `category_id` (Optional[str]): ID of the TargetListCategory.
    - `description` (Optional[str]): Description / notes.
    - `source_campaign_id` (Optional[str]): Source campaign ID.
    - `assigned_user_id` (Optional[str]): ID of the assigned User.
    - `teams_ids` (Optional[List[str]]): List of Team IDs.
    - `custom_fields` (Optional[Dict[str, Any]]): Dictionary of custom fields (must start with `c`).

    Example Requests:
    - Update name and assigned user:
      espo_update_target_list_tool(target_list_id="abc123", name="New List", assigned_user_id="user123")
    - Update category and description:
      espo_update_target_list_tool(target_list_id="abc123", category_id="cat456", description="Updated description")
    - Update custom fields:
      espo_update_target_list_tool(target_list_id="abc123", custom_fields={"c_priority": "High", "c_score": 90})

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(
        f"Request received to update TargetList {target_list_id} with params: {locals()}"
    )

    # Verify API key and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Build params excluding the ID and auth response
    params = build_espo_params(locals(), exclude={"target_list_id", "auth_response"})

    # Include custom fields if provided
    if custom_fields:
        params.update(custom_fields)

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Call PATCH API
    result = client.call_api("PATCH", f"TargetList/{target_list_id}", params=params)
    logger.debug(f"EspoCRM update TargetList result: {result}")
    return result
