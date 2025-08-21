import json, os, time
from airtable_utils import get_records, update_record
import google.generativeai as genai

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are a recruiting analyst. Given this JSON applicant profile:

{applicant_json}

Do four things:
1. Provide a concise 75-word summary.
2. Rate overall candidate quality from 1-10 (higher is better).
3. List any data gaps or inconsistencies you notice.
4. Suggest up to three follow-up questions to clarify gaps.

Return exactly:
Summary: <text>
Score: <integer>
Issues: <comma-separated list or 'None'>
Follow-Ups: <bullet list>
"""

def evaluate_applicant(applicant_id):
    """Call LLM and write results to Applicants table."""

    # Get applicant record
    applicants = get_records("Applicants")
    applicant_record = next((r for r in applicants if r["id"] == applicant_id), None)

    if not applicant_record or "Compressed JSON" not in applicant_record["fields"]:
        print("❌ No JSON found for this applicant.")
        return

    applicant_json = applicant_record["fields"]["Compressed JSON"]

    # Build prompt
    prompt = PROMPT_TEMPLATE.format(applicant_json=applicant_json)

    # Retry up to 3 times (with exponential backoff)
    for attempt in range(3):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            output = response.text.strip()
            break
        except Exception as e:
            print(f"⚠️ LLM call failed (attempt {attempt+1}): {e}")
            time.sleep(2 ** attempt)
    else:
        print("❌ LLM evaluation failed after retries.")
        return

    # Parse response into fields (simple split)
    summary, score, issues, followups = "", "", "", ""
    for line in output.splitlines():
        if line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Score:"):
            score = line.replace("Score:", "").strip()
        elif line.startswith("Issues:"):
            issues = line.replace("Issues:", "").strip()
        elif line.startswith("Follow-Ups:"):
            followups = line.replace("Follow-Ups:", "").strip()

    # Update Airtable
    update_record("Applicants", applicant_id, {
        "LLM Summary": summary,
        "LLM Score": int(score) if score.isdigit() else None,
        "LLM Follow-Ups": followups
    })

    print(f"✅ LLM evaluation updated for applicant {applicant_id}")


if __name__ == "__main__":
    # Example usage
    applicant_id = "recgjRWFrePH7JXNr"  # Replace with real Applicant record ID
    evaluate_applicant(applicant_id)
