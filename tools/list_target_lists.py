from typing import Optional, Dict, Any, List, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("TargetLists")
@doc_name("List TargetLists")
def list_target_lists_tool(
    attribute_select: Annotated[
        Optional[List[str]],
        Field(
            description="List of attributes to return. Limit fields for performance."
        ),
    ] = None,
    bool_filter_list: Annotated[
        Optional[List[str]],
        Field(description="Boolean filters such as ['onlyMy']."),
    ] = None,
    max_size: Annotated[
        Optional[int],
        Field(description="Maximum number of records to return (>= 0 <= 200)."),
    ] = None,
    offset: Annotated[
        Optional[int], Field(description="Pagination offset (>= 0).")
    ] = None,
    order: Annotated[
        Optional[str], Field(description="Sort direction: 'asc' or 'desc'.")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Attribute to sort results by.")
    ] = None,
    text_filter: Annotated[
        Optional[str], Field(description="Text filter query (supports wildcard *)")
    ] = None,
    where_group: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Advanced deepObject filters for complex queries."),
    ] = None,
) -> Dict:
    """
    List TargetList records from EspoCRM with optional filtering, sorting, and pagination.

    Args:
    - `attribute_select` (Optional[List[str]]): Attributes to include in the response to improve performance.
    - `bool_filter_list` (Optional[List[str]]): Boolean filters like `['onlyMy']`.
    - `max_size` (Optional[int]): Maximum number of records to return (0–200).
    - `offset` (Optional[int]): Pagination offset (0-based).
    - `order` (Optional[str]): Sort direction, 'asc' or 'desc'.
    - `order_by` (Optional[str]): Attribute to sort results by.
    - `text_filter` (Optional[str]): Text search query. Supports wildcard `*`.
    - `where_group` (Optional[List[Dict[str, Any]]]): Advanced deepObject filters.

    Example Requests:
    - Fetch first 50 TargetLists with selected attributes:
      `list_target_lists_tool(attribute_select=["name", "assignedUserName"], max_size=50)`
    - Fetch only TargetLists assigned to current user:
      `list_target_lists_tool(bool_filter_list=["onlyMy"])`
    - Fetch TargetLists using advanced whereGroup filter:
      `list_target_lists_tool(where_group=[{"type": "equals", "attribute": "targetStatus", "value": "Listed"}])`

    Returns:
    - A dictionary containing TargetLists data and metadata.
    """
    logger.debug(f"Request received to list TargetLists with params: {locals()}")

    # Check API access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Build query parameters
    params = build_espo_params(locals(), exclude={"auth_response"})

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # GET TargetList records
    result = client.call_api("GET", "TargetList", params=params)
    logger.debug(f"EspoCRM list TargetLists result: {result}")
    return result
