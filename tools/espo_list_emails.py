from typing import Optional, Dict, Any, List, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Emails")
@doc_name("List Emails")
def espo_list_emails_tool(
    attribute_select: Annotated[
        Optional[List[str]],
        Field(
            description="List of Email attributes to return. Select only necessary fields to improve performance."
        ),
    ] = None,
    max_size: Annotated[
        Optional[int],
        Field(
            description="Maximum number of records to return (0–200). Default is 20."
        ),
    ] = 20,
    offset: Annotated[
        Optional[int], Field(description="Pagination offset (>= 0).")
    ] = None,
    order: Annotated[
        Optional[str], Field(description="Sort direction: 'asc' or 'desc'.")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Attribute/field to order by.")
    ] = None,
    text_filter: Annotated[
        Optional[str], Field(description="Text search query. Supports wildcard '*'.")
    ] = None,
    where_group: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Advanced where group (deepObject) filters."),
    ] = None,
    primary_filter: Annotated[
        Optional[str], Field(description="Primary filter if needed.")
    ] = None,
) -> Dict:
    """
    List Email records from EspoCRM with optional filtering, sorting, and pagination.

    Args:
    - `attribute_select` (Optional[List[str]]): Attributes to include in the response.
    - `max_size` (Optional[int]): Maximum number of records to return (0–200).
    - `offset` (Optional[int]): Pagination offset (0-based).
    - `order` (Optional[str]): Sort direction, 'asc' or 'desc'.
    - `order_by` (Optional[str]): Attribute to sort results by.
    - `text_filter` (Optional[str]): Text search query, supports wildcard '*'.
    - `where_group` (Optional[List[Dict[str, Any]]]): Advanced deepObject filters.
    - `primary_filter` (Optional[str]): Primary filter to apply.

    Example Requests:
    - List first 50 emails with selected attributes:
    espo_list_emails_tool(attribute_select=["subject", "fromName", "dateSent"], max_size=50)
    - List emails containing a specific string in subject:
    espo_list_emails_tool(text_filter="*Invoice*")
    - List emails sorted by date sent descending:
    espo_list_emails_tool(order="desc", order_by="dateSent")

    Returns:
    - A dictionary containing emails data and metadata.
    """
    logger.debug(f"Request received to list emails with params: {locals()}")

    # Check API key and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Build query parameters
    params = build_espo_params(locals(), exclude={"auth_response"})

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Call EspoCRM API
    result = client.call_api("GET", "Email", params=params)
    logger.debug(f"EspoCRM list emails result: {result}")
    return result
