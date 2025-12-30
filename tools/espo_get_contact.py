from typing import Dict, Any, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Contacts")
@doc_name("Read Contact")
def espo_get_contact_tool(
    contact_id: Annotated[str, Field(description="The ID of the Contact record to retrieve")]
) -> Dict:
    """
    Read an existing Contact record in EspoCRM.

    This tool retrieves a single Contact record by ID, returning all standard and custom fields.

    Args:
    - `contact_id` (str): The ID of the Contact record.

    Example Requests:
    - Read a contact by ID: espo_read_contact_tool(contact_id="abc123")
    - Read another contact: espo_read_contact_tool(contact_id="xyz789")
    Returns:
    - A structured dict containing the API response with keys:
      `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to read Contact with id: {contact_id}")
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api('GET', f'Contact/{contact_id}')
    logger.debug(f"EspoCRM read contact result: {result}")
    return result
