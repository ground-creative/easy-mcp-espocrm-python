from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Calls")
@doc_name("Delete Call")
def espo_delete_call_tool(
    call_id: Annotated[str, Field(description="ID of the Call record to delete")],
) -> Dict:
    """
    Remove an existing Call record in EspoCRM.

    Args:
    - `call_id` (str): The ID of the Call to remove.

    Example Request:
    - espo_delete_call_tool(call_id="abc123")

    Returns:
    - A structured dict containing the API response with keys:
    `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to delete call with id={call_id}")

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Use canonical instance method which returns a structured dict
    result = client.call_api("DELETE", f"Call/{call_id}")
    logger.debug(f"EspoCRM delete call result: {result}")
    return result
