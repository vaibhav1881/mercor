import json
from airtable_utils import get_records, update_record, create_record

def decompress_applicant(applicant_id):
    """Read compressed JSON and restore data into child tables."""
    
    # Get applicant record
    applicants = get_records("Applicants")
    applicant_record = next((r for r in applicants if r["id"] == applicant_id), None)

    if not applicant_record or "Compressed JSON" not in applicant_record["fields"]:
        print("❌ No JSON found for this applicant.")
        return

    compressed_json = json.loads(applicant_record["fields"]["Compressed JSON"])

    # --- Personal Details (One-to-One) ---
    personal_data = compressed_json.get("personal", {})
    if personal_data:
        personal_data["Applicant ID"] = [applicant_id]
        create_record("Personal Details", personal_data)

    # --- Work Experience (One-to-Many) ---
    for exp in compressed_json.get("experience", []):
        exp["Applicant ID"] = [applicant_id]
        create_record("Work Experience", exp)

    # --- Salary Preferences (One-to-One) ---
    salary_data = compressed_json.get("salary", {})
    if salary_data:
        salary_data["Applicant ID"] = [applicant_id]
        create_record("Salary Preferences", salary_data)

    print(f"✅ Decompressed JSON restored into child tables for {applicant_id}")

if __name__ == "__main__":
    # Example run
    applicant_id = "recgjRWFrePH7JXNr"  # Replace with a real Applicant record ID
    decompress_applicant(applicant_id)
