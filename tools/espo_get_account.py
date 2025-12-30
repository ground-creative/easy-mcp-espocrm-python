from typing import Dict, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI
from app.middleware.AuthenticationMiddleware import check_access
from core.utils.tools import doc_tag, doc_name
from pydantic import Field


@doc_tag("Accounts")
@doc_name("Read Account")
def espo_get_account_tool(
    account_id: Annotated[str, Field(description="ID of the Account record to retrieve")]
) -> Dict:
    """
    Read a single Account record by ID from EspoCRM.

    This tool fetches the full Account entity, including core fields such as
    name, contact details, addresses, ownership, campaign linkage, audit fields,
    and related metadata.

    Args:
    - `account_id` (str): The ID of the Account record to fetch.

    Example Request:
    - Fetch an account by ID:
    espo_get_account_tool(account_id="abc123")

    Returns:
    - A structured dict containing the API response with keys:
    `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to fetch account id={account_id}")

    # Core: verify API key and access permissions
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Core: initialize API client
    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Core: call EspoCRM API to read Account
    result = client.call_api('GET', f'Account/{account_id}')
    logger.debug(f"EspoCRM get account result: {result}")

    return result
