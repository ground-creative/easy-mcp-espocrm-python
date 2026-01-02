from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Emails")
@doc_name("Update Email")
def update_email_tool(
    email_id: str,
    name: Annotated[
        Optional[str], Field(description="Email name (<=255 chars)")
    ] = None,
    subject: Annotated[
        Optional[str], Field(description="Email subject (<=255 chars)")
    ] = None,
    from_string: Annotated[
        Optional[str], Field(description="From string (<=255 chars)")
    ] = None,
    reply_to_string: Annotated[
        Optional[str], Field(description="Reply-To string (<=255 chars)")
    ] = None,
    from_field: Annotated[
        Optional[str], Field(description="From address (<=255 chars)")
    ] = None,
    to: Annotated[Optional[str], Field(description="To address (<=255 chars)")] = None,
    cc: Annotated[
        Optional[str], Field(description="CC addresses (<=255 chars)")
    ] = None,
    bcc: Annotated[
        Optional[str], Field(description="BCC addresses (<=255 chars)")
    ] = None,
    reply_to: Annotated[
        Optional[str], Field(description="Reply-To address (<=255 chars)")
    ] = None,
    person_string_data: Annotated[
        Optional[str], Field(description="Person string data (<=255 chars)")
    ] = None,
    email_address: Annotated[
        Optional[str], Field(description="Primary email address (<=255 chars)")
    ] = None,
    body: Annotated[Optional[str], Field(description="Email body text")] = None,
    is_html: Annotated[
        Optional[bool], Field(description="Set True if body is HTML")
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Email status (Draft, Sending, Sent, Archived, Failed)"),
    ] = None,
    parent_id: Annotated[Optional[str], Field(description="Parent record ID")] = None,
    parent_type: Annotated[
        Optional[str],
        Field(
            description="Parent type (Account, Lead, Contact, Opportunity, Case, CCompany)"
        ),
    ] = None,
    date_sent: Annotated[
        Optional[str], Field(description="Date sent (UTC, YYYY-MM-DD HH:MM:SS)")
    ] = None,
    send_at: Annotated[
        Optional[str],
        Field(description="Scheduled send date (UTC, YYYY-MM-DD HH:MM:SS)"),
    ] = None,
    assigned_user_id: Annotated[
        Optional[str], Field(description="Assigned user ID")
    ] = None,
    replied_id: Annotated[
        Optional[str], Field(description="ID of the email this is replying to")
    ] = None,
    teams_ids: Annotated[
        Optional[List[str]], Field(description="List of Team IDs")
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(description="Custom EspoCRM fields (must start with `c`)"),
    ] = None,
) -> Dict:
    """
    Update an existing Email in EspoCRM.

    This tool updates an Email record by `email_id`. Provide any Email fields to update.
    parameters left as `None` will not be sent to avoid overwriting unchanged values.

    Args:
    - `email_id` (str): ID of the Email record to update.
    - `name` (Optional[str]): Email name (<=255 chars).
    - `subject` (Optional[str]): Email subject (<=255 chars).
    - `from_string` (Optional[str]): From display string (<=255 chars).
    - `reply_to_string` (Optional[str]): Reply-To display string (<=255 chars).
    - `from_field` (Optional[str]): From email address (<=255 chars).
    - `to` (Optional[str]): To email addresses (<=255 chars).
    - `cc` (Optional[str]): CC email addresses (<=255 chars).
    - `bcc` (Optional[str]): BCC email addresses (<=255 chars).
    - `reply_to` (Optional[str]): Reply-To email addresses (<=255 chars).
    - `person_string_data` (Optional[str]): Person string data (<=255 chars).
    - `email_address` (Optional[str]): Primary email address (<=255 chars).
    - `body` (Optional[str]): Email body content (plain text or HTML).
    - `is_html` (Optional[bool]): True if `body` is HTML.
    - `status` (Optional[str]): Email status (Draft, Sending, Sent, Archived, Failed).
    - `parent_id` (Optional[str]): ID of the parent record.
    - `parent_type` (Optional[str]): Type of parent record (Account, Lead, Contact, Opportunity, Case, CCompany).
    - `date_sent` (Optional[str]): Date/time the email was sent (UTC, format: YYYY-MM-DD HH:MM:SS).
    - `send_at` (Optional[str]): Scheduled send date/time (UTC, format: YYYY-MM-DD HH:MM:SS).
    - `assigned_user_id` (Optional[str]): User ID of the assigned owner.
    - `replied_id` (Optional[str]): ID of the email being replied to.
    - `teams_ids` (Optional[List[str]]): List of Team IDs.
    - `custom_fields` (Optional[Dict[str, Any]]): A dictionary of EspoCRM custom fields to update on the Email record. All EspoCRM custom fields are prefixed with `c`.

    Example Requests:
    - Update subject and body: update_email_tool(email_id="abc123", subject="Updated", body="New body")
    - Update parent and status: update_email_tool(email_id="abc123", parent_type="Contact", parent_id="contact456", status="Sent")
    - Update custom fields: update_email_tool(email_id="abc123", custom_fields={"c_processed": True})

    Returns:
    - A structured dict containing the API response with keys:
    `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to update email {email_id} with params: {locals()}")

    # Check api key and address are set in headers
    auth_response = check_access(True)
    if auth_response:
        return auth_response

    params = build_espo_params(locals(), exclude={"email_id", "auth_response"})

    if custom_fields:
        params.update(custom_fields)

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api("PATCH", f"Email/{email_id}", params=params)
    logger.debug(f"EspoCRM update email result: {result}")
    return result
