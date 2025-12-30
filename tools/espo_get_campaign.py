from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from core.utils.tools import doc_tag, doc_name
from pydantic import Field


@doc_tag("Campaigns")
@doc_name("Read Campaign")
def espo_get_campaign_tool(
    campaign_id: Annotated[str, Field(description="ID of the Campaign record to retrieve")]
) -> Dict:
    """
    Get a single Campaign record by ID from EspoCRM.

    Args:
    - `campaign_id` (str): The ID of the Campaign to fetch.

    Example Request:
    - espo_get_campaign_tool(campaign_id="abc123")

    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to fetch campaign id={campaign_id}")

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Call the Campaign endpoint
    result = client.call_api('GET', f'Campaign/{campaign_id}')
    logger.debug(f"EspoCRM get campaign result: {result}")
    return result
