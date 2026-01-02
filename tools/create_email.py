from typing import Dict, Any, List, Optional, Annotated
from core.utils.logger import logger
from core.utils.state import global_state
from app.utils.espo_helpers import EspoAPI, build_espo_params
from app.middleware.AuthenticationMiddleware import check_access
from pydantic import Field
from core.utils.tools import doc_tag, doc_name


@doc_tag("Emails")
@doc_name("Create Email")
def create_email_tool(
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
    from_: Annotated[
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
    duplicate_source_id: Annotated[
        Optional[str],
        Field(
            description="Record ID being duplicated, sent as X-Duplicate-Source-Id header"
        ),
    ] = None,
    skip_duplicate_check: Annotated[
        Optional[bool],
        Field(
            description="Skip duplicate check, sent as X-Skip-Duplicate-Check header"
        ),
    ] = None,
    custom_fields: Annotated[
        Optional[Dict[str, Any]],
        Field(description="Custom EspoCRM fields starting with `c`"),
    ] = None,
) -> Dict:
    """
    Create a new Email in EspoCRM.

    This tool creates an Email record using standard Email fields. Any parameter set to `None` is omitted from the request to avoid overwriting defaults.

    Args:
    - `name` (Optional[str]): Email name (<=255 chars).
    - `subject` (Optional[str]): Email subject line (<=255 chars).
    - `from_` (Optional[str]): From display string (<=255 chars).
    - `reply_to_string` (Optional[str]): Reply-To display string (<=255 chars).
    - `from` (Optional[str]): From email address (<=255 chars).
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
    - `duplicate_source_id` (Optional[str]): Record ID of an email being duplicated. Sent as header `X-Duplicate-Source-Id`.
    - `skip_duplicate_check` (Optional[bool]): Skip duplicate check, sent as header `X-Skip-Duplicate-Check`.
    - `custom_fields` (Optional[Dict[str, Any]]): Custom fields to update on the Email record (must start with `c`).

    Example Requests:
    - Create a basic email: create_email_tool(subject="Hello", to="recipient@example.com", body="This is a test email.")
    - Create an email with HTML body and parent Contact: create_email_tool(subject="Welcome", to="user@example.com", body="<p>Hello!</p>", is_html=True, parent_type="Contact", parent_id="abc123")
    - Create an email with a custom field: create_email_tool(subject="Custom", to="user@example.com", custom_fields={"c_custom_flag": True})

    Returns:
    - `Dict`: Structured dict containing the API response with keys `status_code`, `ok`, `data`, `error`, and `error_type`.
    """
    logger.info(f"Request received to create email with params: {locals()}")

    auth_response = check_access(True)
    if auth_response:
        return auth_response

    # Exclude header-only params from body
    params = build_espo_params(
        locals(),
        exclude={"duplicate_source_id", "skip_duplicate_check", "auth_response"},
    )

    if "from_" in params:
        params["from"] = params.pop("from_")

    # Prepare headers for duplicate handling
    extra_headers = {}
    if duplicate_source_id:
        extra_headers["X-Duplicate-Source-Id"] = str(duplicate_source_id)
    if skip_duplicate_check is not None:
        extra_headers["X-Skip-Duplicate-Check"] = (
            "true" if skip_duplicate_check else "false"
        )

    api_key = global_state.get("api_key")
    api_address = global_state.get("api_address")
    client = EspoAPI(api_address, api_key)

    result = client.call_api(
        "POST",
        "Email",
        params=params,
        extra_headers=extra_headers if extra_headers else None,
    )
    logger.debug(f"EspoCRM create email result: {result}")
    return result
