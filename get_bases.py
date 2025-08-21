import requests
import json
from config import HEADERS

def get_bases():
    """Fetches and prints the list of accessible Airtable bases."""
    url = "https://api.airtable.com/v0/meta/bases"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        bases_data = response.json()
        
        print("✅ Successfully fetched your Airtable bases:\n")
        for base in bases_data.get("bases", []):
            print(f"  - Name: {base['name']}")
            print(f"    ID:   {base['id']}\n")

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
        print("Please check your AIRTABLE_API_KEY in the .env file.")
    except Exception as err:
        print(f"❌ An other error occurred: {err}")

if __name__ == "__main__":
    get_bases()
