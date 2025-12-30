from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from core.utils.tools import doc_tag, doc_name
from pydantic import Field


@doc_tag("Calls")
@doc_name("Read Call")
def espo_get_call_tool(
    call_id: Annotated[str, Field(description="ID of the Call record to retrieve")],
) -> Dict:
    """
    Get a single Call record by ID from EspoCRM.

    This tool retrieves an existing Call record, including metadata, participants,
    related entities, and timestamps.

    Args:
    - `call_id` (str): The ID of the Call record to fetch.

    Example Request:
    - espo_get_call_tool(call_id="abc123")

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to fetch call id={call_id}")

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Fetch Call record by ID
    result = client.call_api("GET", f"Call/{call_id}")
    logger.debug(f"EspoCRM get call result: {result}")
    return result
