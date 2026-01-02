from typing import Dict
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from typing import Annotated
from core.utils.tools import doc_tag, doc_name


@doc_tag("Contacts")
@doc_name("Delete Contact")
def delete_contact_tool(
    contact_id: Annotated[
        str, Field(description="The ID of the Contact record to delete")
    ],
) -> Dict:
    """
    Delete an existing Contact in EspoCRM.

    This tool removes a Contact record permanently from EspoCRM.

    Args:
    - `contact_id` (str): The ID of the Contact record to delete.

    Example Requests:
    - Delete a contact: delete_contact_tool(contact_id="abc123")

    Returns:
    - A structured dict containing the API response with keys: `status_code`, `ok`, `data`, `error`, `error_type`.
      The `data` field is always True if deletion succeeded.
    """
    logger.info(f"Request received to delete Contact with id: {contact_id}")
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api("DELETE", f"Contact/{contact_id}")
    logger.debug(f"EspoCRM delete contact result: {result}")
    return result
