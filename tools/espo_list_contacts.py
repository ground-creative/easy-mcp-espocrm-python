from typing import Dict, Any, List, Optional, Union, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Contacts")
@doc_name("List Contacts")
def espo_list_contacts_tool(
    attribute_select: Annotated[Optional[List[str]], Field(description="Attributes to return. Only select necessary ones to improve performance")] = None,
    bool_filter_list: Annotated[Optional[List[str]], Field(description="Bool filters. Allowed value: onlyMy")] = None,
    max_size: Annotated[Optional[int], Field(description="Maximum number of records to return. 0-200")] = 100,
    offset: Annotated[Optional[int], Field(description="Pagination offset. >=0")] = 0,
    order: Annotated[Optional[str], Field(description="Order direction. Allowed values: asc, desc")] = None,
    order_by: Annotated[Optional[str], Field(description="Attribute to order by")] = None,
    primary_filter: Annotated[Optional[str], Field(description="Primary filter. Allowed values: portalUsers, notPortalUsers, accountActive")] = None,
    text_filter: Annotated[Optional[str], Field(description="Text filter query. Wildcard (*) is supported")] = None,
    where_group: Annotated[Optional[List[Dict[str, Any]]], Field(description="Where conditions. Each item: {type, attribute, operator, value}")] = None,
    type_filter: Annotated[Optional[str], Field(description="Record type")] = None,
    date_time: Annotated[Optional[bool], Field(description="Set true for date-time fields")] = None,
    time_zone: Annotated[Optional[str], Field(description="Time zone for date-time fields")] = None,
    x_no_total: Annotated[Optional[bool], Field(description="Disable calculation of total number of records")] = None,
) -> Dict:
    """
    List Contact records in EspoCRM.

    This tool retrieves Contact records with optional filtering, ordering, and pagination. Supports deep filtering and selective attributes to improve performance.

    Args:
    - `attribute_select` (Optional[List[str]]): Attributes to return. Allowed values: salutationName, firstName, lastName, middleName, name, accountAnyId, title, description, emailAddressIsOptedOut, emailAddressIsInvalid, emailAddress, emailAddressData, phoneNumberIsOptedOut, phoneNumberIsInvalid, phoneNumber, phoneNumberData, doNotCall, addressStreet, addressCity, addressState, addressCountry, addressPostalCode, accountId, accountName, accountsIds, accountsColumns, accountsNames, accountRole, accountIsInactive, accountType, opportunityRole, acceptanceStatus, acceptanceStatusMeetings, acceptanceStatusCalls, campaignId, campaignName, createdAt, modifiedAt, createdById, createdByName, modifiedById, modifiedByName, assignedUserId, assignedUserName, teamsIds, teamsNames, targetListsIds, targetListsNames, targetListId, targetListName, portalUserId, portalUserName, hasPortalUser, originalLeadId, originalLeadName, targetListIsOptedOut, originalEmailId, originalEmailName, addressMap, streamUpdatedAt
    - `bool_filter_list` (Optional[List[str]]): Boolean filters. Allowed: onlyMy
    - `max_size` (Optional[int]): Max records to return (0-200)
    - `offset` (Optional[int]): Pagination offset
    - `order` (Optional[str]): Order direction, asc or desc
    - `order_by` (Optional[str]): Attribute to order by
    - `primary_filter` (Optional[str]): Primary filter, allowed: portalUsers, notPortalUsers, accountActive
    - `text_filter` (Optional[str]): Text filter query, wildcard (*) supported
    - `where_group` (Optional[List[Dict[str, Any]]]): Where conditions [{type, attribute, operator, value}]
    - `type_filter` (Optional[str]): Record type
    - `date_time` (Optional[bool]): Set true for date-time fields
    - `time_zone` (Optional[str]): Time zone for date-time fields
    - `x_no_total` (Optional[bool]): Disable total count calculation

    Example Requests:
    - List first 50 contacts: espo_list_contacts_tool(max_size=50)
    - List contacts with only my records and select names: espo_list_contacts_tool(attribute_select=["firstName","lastName"], bool_filter_list=["onlyMy"])
    - List contacts with text filter and order by last name: espo_list_contacts_tool(text_filter="Acme*", order_by="lastName", order="asc")

    Returns:
    - A structured dict containing the API response with keys: `status_code`, `ok`, `data`, `error`, `error_type`, `total`.
    """
    logger.info(f"Request received to list contacts with params: {locals()}")
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    params = build_espo_params(locals(), exclude={"auth_response"})
    extra_headers = {}
    
    if x_no_total is not None:
        extra_headers["X-No-Total"] = "true" if x_no_total else "false"

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api('GET', 'Contact', params=params, extra_headers=extra_headers if extra_headers else None)
    logger.debug(f"EspoCRM list contacts result: {result}")
    return result
