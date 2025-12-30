# Easy MCP EspoCRM Tools

This is a set of tools for espoCRM to be used with easy mcp server.<br>
https://github.com/ground-creative/easy-mcp-python

## Key Features

- **Document Creation**: Create Google Docs with custom titles and content.
- **Spreadsheet Management**: Create and edit Google Sheets, including adding and deleting rows.
- **File Upload**: Upload text, JSON, or CSV files to Google Drive with custom titles.
- **Folder Organization**: Create and manage folders to structure your Drive content.
- **Item Management**: Move, delete (with confirmation), or list files and folders.
- **File Access**: Retrieve file content and view detailed information.

## Authentication

To use the EspoCRM API u need an api key and the server address.

## Installation

1. Clone the repository from the root folder of the easy mcp installation:

```
git clone https://github.com/ground-creative/easy-mcp-espocrm-python.git app
```

2. Install requirements:

```
pip install -r app/requirements.txt
```

3. Add parameters to env file:

```
TEST_API_KEY=__YOUR_ESPOCRM_API_KEY__
TEST_API_ADDRESS=__YOUR_ESPOCRM_SERVER_ADDRESS__
```

4. Run the server:

```
# Run via fastapi wrapper
python3 run.py -s fastapi
```

## Available MCP Tools

The following tools are provided by this MCP server:

## Tools and Specifications

| Tool Name            | Description                                                                                              | Parameters Required                                                                 |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Get Lead             | Retrieve a single Lead record by ID from EspoCRM.                                                        | `lead_id` (str)                                                                     |
| List Leads           | List leads with filtering, pagination, sorting and advanced `where_group` deepObject filters.            | `attribute_select` (Optional[list]), `bool_filter_list` (Optional[list]), `max_size` (Optional[int, 0-200]), `offset` (Optional[int]), `order` (Optional[str]), `order_by` (Optional[str]), `primary_filter` (Optional[str]), `text_filter` (Optional[str]), `where_group` (Optional[list of dicts]) |
| Create Lead          | Create a new Lead with common Lead fields and optional duplicate-handling headers.                      | Optional: `salutation_name`, `first_name`, `middle_name`, `last_name`, `title`, `status`, `source`, `industry`, `opportunity_amount`, `opportunity_amount_currency`, `website`, `address_street`, `address_city`, `address_state`, `address_country`, `address_postal_code`, `email_address`, `email_address_data`, `phone_number`, `phone_number_data`, `do_not_call`, `description`, `account_name`, `assigned_user_id`, `teams_ids`, `campaign_id`, `target_list_id`, `duplicate_source_id` (header), `skip_duplicate_check` (header) |
| Update Lead          | Update an existing Lead. Only provided parameters are sent;         | `lead_id` (str), plus same optional fields as Create Lead                             |
| Delete Lead          | Delete a Lead by ID.                                                                                     | `lead_id` (str)                                                                     |


# Screenshots

Server info page:
![Server info page](screenshots/1.png)

Google oAuth page
![Google oAuth page](screenshots/3.png)

Google permission scopes page
![Google psermission scopes page](screenshots/4.png)

User authenticated page
![User Aunthenticated page](screenshots/5.png)
