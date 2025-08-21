from airtable_utils import create_record

def add_mock_applicant():
    # Step 1: Create Applicant
    applicant = create_record("Applicants", {"Shortlist Status": "Pending"})
    applicant_id = applicant["id"]
    print(f"✅ Created Applicant {applicant_id}")

    # Step 2: Personal Details
    create_record("Personal Details", {
        "Applicant ID": [applicant_id],
        "Full Name": "Rohit Sharma",
        "Email": "rohit.sharma@example.com",
        "Location": "India",
        "LinkedIn": "https://linkedin.com/in/rohitsharma"
    })

    # Step 3: Work Experience
    create_record("Work Experiences", {
        "Applicant ID": [applicant_id],
        "Company": "Google",
        "Title": "Software Engineer",
        "Start Date": "2018-01-01",
        "End Date": "2022-12-31",
        "Technologies": ["Python", "React", "AWS"]
    })

    # Step 4: Salary Preferences
    create_record("Salary Preferences", {
        "Applicant ID": [applicant_id],
        "Preferred Rate": 90,
        "Minimum Rate": 70,
        "Currency": "USD",
        "Availability (hrs/wk)": 25
    })

    print("✅ Mock applicant added successfully.")
    return applicant_id

if __name__ == "__main__":
    add_mock_applicant()
