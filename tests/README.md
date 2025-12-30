# Running Tests

## Installation

1. Add variables .env in root folder:

```
TEST_API_KEY=add a test api key
```

2. Install `pytest` library:

```
pip install pytest==8.3.5
```

3. Run the tests inside app/tests folder:

```
# Run all tests
pytest

# Print to console 
pytest -s

# Run all test of file
pytest test_leads.py

# Run specific test
pytest test_leads.py::test_espo_list_leads_tool
```
