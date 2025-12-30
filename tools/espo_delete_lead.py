from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from core.utils.tools import doc_tag
from pydantic import Field


@doc_tag("Leads")
def espo_delete_lead_tool(
    lead_id: Annotated[str, Field(description="ID of the Lead record to delete")],
) -> Dict:
    """
    Remove an existing Lead record in EspoCRM.

    Args:
    - `lead_id` (str): The ID of the Lead to remove.

    Example:
    - `espo_delete_lead_tool(lead_id="abc123")`

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to delete lead with id={lead_id}")

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Use the canonical instance method which returns a structured dict
    result = client.call_api('DELETE', f'Lead/{lead_id}')
    logger.debug(f"EspoCRM delete lead result: {result}")
    return result
