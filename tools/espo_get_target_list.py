from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from core.utils.tools import doc_tag, doc_name
from pydantic import Field


@doc_tag("TargetLists")
@doc_name("Read TargetList")
def espo_get_target_list_tool(
    target_list_id: Annotated[
        str, Field(description="ID of the TargetList record to retrieve")
    ],
) -> Dict:
    """
    Get a single TargetList record by ID from EspoCRM.

    Args:
    - `target_list_id` (str): The ID of the TargetList to fetch.

    Example Request:
    - espo_get_target_list_tool(target_list_id="abc123")

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to fetch TargetList id={target_list_id}")

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Call EspoCRM API
    result = client.call_api("GET", f"TargetList/{target_list_id}")
    logger.debug(f"EspoCRM get TargetList result: {result}")
    return result
