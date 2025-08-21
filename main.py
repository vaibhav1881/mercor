import json
from airtable_utils import get_records
from compress import compress_applicant
from shortlist import shortlist_applicant
from llm_eval import evaluate_applicant

def run_pipeline():
    """Run compression → shortlist → LLM evaluation for all applicants."""
    
    applicants = get_records("Applicants")
    print(f"🔎 Found {len(applicants)} applicants in Airtable.")

    for applicant in applicants:
        applicant_id = applicant["id"]
        print(f"\n🚀 Processing Applicant: {applicant_id}")

        # Step 3: Compression
        compressed = compress_applicant(applicant_id)

        # Step 5: Shortlist
        shortlist_applicant(applicant_id)

        # Step 6: LLM Evaluation
        evaluate_applicant(applicant_id)

    print("\n✅ Pipeline complete for all applicants.")

if __name__ == "__main__":
    run_pipeline()
