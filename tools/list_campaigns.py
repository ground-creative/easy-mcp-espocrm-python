from typing import Optional, Dict, Any, List, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Campaigns")
@doc_name("List Campaigns")
def list_campaigns_tool(
    attribute_select: Annotated[
        Optional[List[str]],
        Field(
            description="List of attributes to return. Use to limit fields and improve performance."
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
        Optional[str], Field(description="Primary filter: active")
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
    List campaigns from EspoCRM with optional filtering, sorting, and pagination.

    This tool fetches campaigns with advanced query options such as attribute selection, boolean filters,
    pagination, sorting, and deep where group conditions.

    Args:
    - `attribute_select` (Optional[List[str]]): Attributes to include in the response to improve performance.
    - `bool_filter_list` (Optional[List[str]]): Boolean filters such as `['onlyMy']`.
    - `max_size` (Optional[int]): Maximum number of records to return (0–200). Overrides page_size if provided.
    - `offset` (Optional[int]): Pagination offset (0-based). If not set, computed from page and page_size.
    - `order` (Optional[str]): Sort direction, either `'asc'` or `'desc'`.
    - `order_by` (Optional[str]): Attribute to sort results by.
    - `primary_filter` (Optional[str]): Primary filter to use. Allowed values depend on your EspoCRM setup (e.g., `'active'`, `'completed'`).
    - `text_filter` (Optional[str]): Text search query. Supports wildcard `*`.
    - `where_group` (Optional[List[Dict[str, Any]]]): Advanced deepObject filters for complex queries.

    Example Requests:
    - Fetch first 50 campaigns with only selected attributes:
    list_campaigns_tool(attribute_select=["name", "status"], max_size=50)
    - Fetch campaigns assigned only to the current user, sorted by creation date descending:
    list_campaigns_tool(bool_filter_list=["onlyMy"], order="desc", order_by="createdAt")
    - Fetch campaigns using advanced whereGroup filter:
    list_campaigns_tool(where_group=[{"type": "equals", "attribute": "status", "value": "Active"}, {"type": "contains", "attribute": "name", "value": "Launch"}])
    - Fetch campaigns with a primary filter:
    list_campaigns_tool(primary_filter="completed", max_size=20)
    - Fetch campaigns using a text search query:
    list_campaigns_tool(text_filter="Summer*2026", max_size=10)

    Returns:
    - A dictionary containing campaigns data and metadata.
    """
    logger.debug(f"Request received to list campaigns with params: {locals()}")

    # Check api key and address are set in headers
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    params = build_espo_params(locals(), exclude={"auth_response"})

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)
    result = client.call_api("GET", "Campaign", params=params)
    logger.debug(f"EspoCRM list campaigns result: {result}")
    return result
