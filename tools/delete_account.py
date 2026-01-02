from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Accounts")
@doc_name("Delete Account")
def delete_account_tool(
    account_id: Annotated[str, Field(description="ID of the Account record to delete")],
) -> Dict:
    """
    Remove an existing Account record in EspoCRM.

    Args:
    - `account_id` (str): The ID of the Account to remove.

    Example Request:
    - delete_account_tool(account_id="abc123")

    Returns:
    - A structured dict containing the API response with keys:
    `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to delete account with id={account_id}")

    # Verify API configuration and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Use the canonical instance method which returns a structured dict
    result = client.call_api("DELETE", f"Account/{account_id}")
    logger.debug(f"EspoCRM delete account result: {result}")
    return result
