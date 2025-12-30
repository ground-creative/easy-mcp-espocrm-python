from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Users")
@doc_name("List Users")
def espo_list_users_tool(
    attribute_select: Annotated[
        Optional[List[str]],
        Field(
            description="List of User attributes to return. Select only necessary ones to improve performance."
        ),
    ] = None,
    bool_filter_list: Annotated[
        Optional[List[str]],
        Field(description="Boolean filter flags, e.g., ['onlyMyTeam']"),
    ] = None,
    max_size: Annotated[
        Optional[int], Field(description="Maximum number of records to return (0-200)")
    ] = None,
    offset: Annotated[
        Optional[int], Field(description="Pagination offset (>=0)")
    ] = None,
    order: Annotated[
        Optional[str], Field(description="Sort direction: 'asc' or 'desc'")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Attribute/field to order by")
    ] = None,
    primary_filter: Annotated[
        Optional[str],
        Field(description="Primary filter, e.g., 'active', 'portal', 'api'"),
    ] = None,
    text_filter: Annotated[
        Optional[str], Field(description="Text filter query. Wildcard (*) is supported")
    ] = None,
    where_group: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Advanced where group filters for complex queries"),
    ] = None,
    x_no_total: Annotated[
        Optional[bool],
        Field(description="Disable calculation of total records if True"),
    ] = None,
) -> Dict:
    """
    List User records in EspoCRM.

    Args:
    - `attribute_select` (Optional[List[str]]): List of User fields to include in the response.
    - `bool_filter_list` (Optional[List[str]]): Boolean filters such as `['onlyMyTeam']`.
    - `max_size` (Optional[int]): Maximum number of records to return (0-200).
    - `offset` (Optional[int]): Pagination offset (0-based).
    - `order` (Optional[str]): Sort direction: 'asc' or 'desc'.
    - `order_by` (Optional[str]): Attribute to sort by.
    - `primary_filter` (Optional[str]): Primary filter value.
    - `text_filter` (Optional[str]): Text search query. Supports wildcard '*'.
    - `where_group` (Optional[List[Dict[str, Any]]]): Deep object filters for complex queries.
    - `x_no_total` (Optional[bool]): Disable total count calculation if True.

    Example Requests:
    - List all users:
    espo_list_users_tool()
    - List users with only first and last names:
    espo_list_users_tool(attribute_select=["firstName", "lastName"])
    - List active users only:
    espo_list_users_tool(primary_filter="active")

    Returns:
    - A dictionary with the API response containing keys: `status_code`, `ok`, `data`, `error`, `error_type`.
    """
    logger.info(f"Request received to list users with params: {locals()}")

    # Check API key and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Build query parameters
    params = build_espo_params(locals(), exclude={"x_no_total", "auth_response"})

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    # Add header to disable total if requested
    headers = {"X-No-Total": "true"} if x_no_total else None

    # Call EspoCRM API
    result = client.call_api("GET", "User", params=params, extra_headers=headers)
    logger.debug(f"EspoCRM list users result: {result}")
    return result
