from typing import Optional, Dict, Any, List, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Calls")
@doc_name("List Calls")
def list_calls_tool(
    attribute_select: Annotated[
        Optional[List[str]],
        Field(
            description="Attributes to return. Select only the necessary ones to improve performance."
        ),
    ] = None,
    bool_filter_list: Annotated[
        Optional[List[str]],
        Field(description="Boolean filter flags (e.g. ['onlyMy'])."),
    ] = None,
    max_size: Annotated[
        Optional[int],
        Field(description="Maximum number of records to return (>= 0 <=200)"),
    ] = None,
    offset: Annotated[
        Optional[int], Field(description="Pagination offset (>= 0).")
    ] = None,
    order: Annotated[
        Optional[str], Field(description="Sort direction: 'asc' or 'desc'.")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Attribute/field to order by.")
    ] = None,
    primary_filter: Annotated[
        Optional[str], Field(description="Primary filter: planned|held|todays")
    ] = None,
    text_filter: Annotated[
        Optional[str], Field(description="Text filter query (supports wildcard *)")
    ] = None,
    where_group: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Advanced where group (deepObject) filters."),
    ] = None,
) -> Dict:
    """
    List Calls from EspoCRM with optional filtering, sorting, and pagination.

    Args:
    - `attribute_select` (Optional[List[str]]): Attributes to include in the response to improve performance.
    - `bool_filter_list` (Optional[List[str]]): Boolean filters such as `['onlyMy']`.
    - `max_size` (Optional[int]): Maximum number of records to return (0–200).
    - `offset` (Optional[int]): Pagination offset (0-based).
    - `order` (Optional[str]): Sort direction, either `'asc'` or `'desc'`.
    - `order_by` (Optional[str]): Attribute to sort results by.
    - `primary_filter` (Optional[str]): Primary filter to use. Allowed: `'planned'`, `'held'`, `'todays'`.
    - `text_filter` (Optional[str]): Text search query. Supports wildcard `*`.
    - `where_group` (Optional[List[Dict[str, Any]]]): Advanced deepObject filters for complex queries.

    Example Requests:
    - Fetch first 50 calls with only selected attributes:
        list_calls_tool(attribute_select=["name", "dateStart"], max_size=50)
    - Fetch calls assigned to current user only (bool filter):
        list_calls_tool(bool_filter_list=["onlyMy"], max_size=100)
    - Fetch today's planned calls:
        list_calls_tool(primary_filter="todays", primary_filter="planned")
    - Fetch outbound calls using a where_group filter:
        list_calls_tool(where_group=[{"type": "equals", "attribute": "direction", "value": "Outbound"}])
    - Fetch calls filtered by parent (Account) and paginated:
        list_calls_tool(where_group=[{"type":"equals","attribute":"parentType","value":"Account"},{"type":"equals","attribute":"parentId","value":"<ACCOUNT_ID>"}], max_size=25, offset=50)

    Returns:
    - A dictionary containing calls data and metadata.
    """
    logger.debug(f"Request received to list calls with params: {locals()}")

    # Check api key and address are set in headers
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    params = build_espo_params(locals(), exclude={"auth_response"})

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)
    result = client.call_api("GET", "Call", params=params)
    logger.debug(f"EspoCRM list calls result: {result}")
    return result
