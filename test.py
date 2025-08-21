
import requests, os

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")

url = f"https://api.airtable.com/v0/{BASE_ID}/Work%20Experiences"
headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

resp = requests.get(url, headers=headers)
print(resp.status_code, resp.text)
