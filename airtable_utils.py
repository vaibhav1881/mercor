import requests
from config import BASE_ID, HEADERS

def get_records(table):
    """Fetch all records from a given table."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["records"]

def update_record(table, record_id, fields):
    """Update a record with new field values."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table}/{record_id}"
    data = {"fields": fields}
    response = requests.patch(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()

def create_record(table, fields):
    """Create a new record in a table."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table}"
    data = {"fields": fields}
    response = requests.post(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()
