from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from core.utils.tools import doc_tag, doc_name
from pydantic import Field


@doc_tag("Emails")
@doc_name("Read Email")
def espo_get_email_tool(
    email_id: Annotated[str, Field(description="ID of the Email record to retrieve")],
) -> Dict:
    """
    Get a single Email record by ID from EspoCRM.

    Args:
    - `email_id` (str): The ID of the Email to fetch.

    Example Request:
    - espo_get_email_tool(email_id="email123")

    Returns:
    - A structured dict containing the API response with keys:
    `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to fetch email id={email_id}")

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Fetch the email record
    result = client.call_api("GET", f"Email/{email_id}")
    logger.debug(f"EspoCRM get email result: {result}")
    return result
