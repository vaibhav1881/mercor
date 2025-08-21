import json
from airtable_utils import get_records, update_record

def compress_applicant(applicant_id):
    """Build a compressed JSON profile for a given applicant."""
    
    # Fetch related records
    personal = [r["fields"] for r in get_records("Personal Details") if applicant_id in r["fields"].get("Applicant ID", [])]
    work = [r["fields"] for r in get_records("Work Experiences") if applicant_id in r["fields"].get("Applicant ID", [])]
    salary = [r["fields"] for r in get_records("Salary Preferences") if applicant_id in r["fields"].get("Applicant ID", [])]

    # Build JSON
    compressed = {
        "personal": personal[0] if personal else {},
        "experience": work,
        "salary": salary[0] if salary else {}
    }

    # Save back to Applicants table
    update_record("Applicants", applicant_id, {"Compressed JSON": json.dumps(compressed, indent=2)})
    print(f"✅ Compressed JSON updated for applicant {applicant_id}")

    return compressed

if __name__ == "__main__":
    # Example run
    applicant_id = "recgjRWFrePH7JXNr"  # Replace with real Airtable Applicant record ID
    compress_applicant(applicant_id)
