from typing import Optional, Dict, Any, List, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Accounts")
@doc_name("List Accounts")
def espo_list_accounts_tool(
    # Core query controls
    attribute_select: Annotated[
        Optional[List[str]],
        Field(description="Attributes to return. Use to limit fields and improve performance."),
    ] = None,
    bool_filter_list: Annotated[
        Optional[List[str]],
        Field(description="Boolean filter flags (e.g. ['onlyMy'])."),
    ] = None,
    max_size: Annotated[
        Optional[int],
        Field(description="Maximum number of records to return (>=0 <=200)."),
    ] = None,
    offset: Annotated[
        Optional[int],
        Field(description="Pagination offset (>=0)."),
    ] = None,
    order: Annotated[
        Optional[str],
        Field(description="Sort direction: 'asc' or 'desc'."),
    ] = None,
    order_by: Annotated[
        Optional[str],
        Field(description="Attribute/field to order by."),
    ] = None,
    primary_filter: Annotated[
        Optional[str],
        Field(description="Primary filter (customers, resellers, partners, recentlyCreated)."),
    ] = None,
    text_filter: Annotated[
        Optional[str],
        Field(description="Text filter query (supports wildcard *)."),
    ] = None,
    where_group: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description="Advanced where group (deepObject) filters."),
    ] = None,
    no_total: Annotated[
        Optional[bool],
        Field(description="Disable total count. Sent as header 'X-No-Total' (true/false)."),
    ] = None,
) -> Dict:
    """
    List Account records from EspoCRM with filtering, sorting, and pagination.

    This tool retrieves Account records using EspoCRM list API features such as attribute
    selection, boolean filters, pagination, ordering, text search, and advanced whereGroup
    conditions.

    Args:
    - `attribute_select` (Optional[List[str]]): Attributes to include in the response.
    - `bool_filter_list` (Optional[List[str]]): Boolean filters (e.g. ['onlyMy']).
    - `max_size` (Optional[int]): Maximum number of records to return (0–200).
    - `offset` (Optional[int]): Pagination offset (0-based).
    - `order` (Optional[str]): Sort direction ('asc' or 'desc').
    - `order_by` (Optional[str]): Field to sort by.
    - `primary_filter` (Optional[str]): Primary filter (customers, resellers, partners, recentlyCreated).
    - `text_filter` (Optional[str]): Text search query (supports '*').
    - `where_group` (Optional[List[Dict[str, Any]]]): Advanced deepObject filters.
    - `no_total` (Optional[bool]): Disable total count calculation.

    Example Requests:
    - List first 50 accounts with selected fields:
      espo_list_accounts_tool(attribute_select=["name", "website", "emailAddress"], max_size=50)
    - List only my accounts, newest first:
      espo_list_accounts_tool(bool_filter_list=["onlyMy"], order="desc", order_by="createdAt")
    - Search accounts by name:
      espo_list_accounts_tool(text_filter="Acme*") 
    - Use advanced whereGroup filtering:
      espo_list_accounts_tool(where_group=[{"type": "equals", "attribute": "industry", "value": "Technology"}])

    Returns:
    - A structured dict containing:
      `total`, `list`, `status_code`, `ok`, `error`, and `error_type`.
    """
    logger.debug(f"Request received to list accounts with params: {locals()}")

    # Check API key and access
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Build query params (exclude header-only values)
    params = build_espo_params(locals(), exclude={"auth_response", "no_total"})

    # Optional headers
    extra_headers = {}
    if no_total is not None:
        extra_headers["X-No-Total"] = "true" if no_total else "false"

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api(
        'GET',
        'Account',
        params=params,
        extra_headers=extra_headers if extra_headers else None,
    )
    logger.debug(f"EspoCRM list accounts result: {result}")
    return result
