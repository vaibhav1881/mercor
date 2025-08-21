import json
from airtable_utils import get_records, create_record

# Tier-1 company list
TIER1_COMPANIES = ["Google", "Meta", "OpenAI", "Microsoft", "Amazon", "Apple"]

# Allowed locations
ALLOWED_LOCATIONS = ["US", "United States", "Canada", "UK", "United Kingdom", "Germany", "India"]

def calculate_experience(experiences):
    """Very simple experience calculation based on number of roles * 2 years each (placeholder)."""
    # In a real setup, you'd calculate exact years from start/end dates
    return len(experiences) * 2

def shortlist_applicant(applicant_id):
    """Check rules and insert into Shortlisted Leads if passed."""
    
    applicants = get_records("Applicants")
    applicant_record = next((r for r in applicants if r["id"] == applicant_id), None)

    if not applicant_record or "Compressed JSON" not in applicant_record["fields"]:
        print("❌ No JSON found for this applicant.")
        return

    data = json.loads(applicant_record["fields"]["Compressed JSON"])

    personal = data.get("personal", {})
    experiences = data.get("experience", [])
    salary = data.get("salary", {})

    # --- Rule Checks ---
    exp_years = calculate_experience(experiences)
    has_tier1 = any(exp.get("Company") in TIER1_COMPANIES for exp in experiences)

    exp_ok = exp_years >= 4 or has_tier1
    comp_ok = salary.get("Preferred Rate", 9999) <= 100 and salary.get("Availability (hrs/wk)", 0) >= 20
    loc_ok = any(loc in personal.get("Location", "") for loc in ALLOWED_LOCATIONS)

    # --- Decision ---
    if exp_ok and comp_ok and loc_ok:
        reason = f"Experience OK ({exp_years} yrs or Tier-1: {has_tier1}), Rate OK, Location OK"
        create_record("Shortlisted Leads", {
            "Applicant ID": [applicant_id],
            "Compressed JSON": json.dumps(data, indent=2),
            "Score Reason": reason
        })
        print(f"✅ Applicant {applicant_id} shortlisted.")
    else:
        print(f"⚠️ Applicant {applicant_id} did not meet criteria.")

if __name__ == "__main__":
  
    applicant_id = "recgjRWFrePH7JXNr"  
    shortlist_applicant(applicant_id)
