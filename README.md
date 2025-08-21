# Mercor Tooling Airtable Exercise

## 📌 Project Overview
This project is a **mini-interview task** for Mercor, designed to demonstrate skills in Airtable schema design, Python automation, JSON data handling, and LLM integration.

The goal is to build a complete pipeline that:
1. Collects contractor application data using **multi-table forms** in Airtable.
2. Compresses normalized data into a **single JSON object** stored in the Applicants table.
3. Decompresses JSON back into normalized child tables when needed.
4. Automatically shortlists promising candidates based on **multi-factor rules**.
5. Uses an **LLM endpoint** (e.g., OpenAI GPT) to evaluate, enrich, and sanity-check applications.

---

## 🗂️ Airtable Base Setup

The Airtable base consists of **five tables**:

### 1. Applicants (Parent)
- `Applicant ID` (Primary field, Autonumber)
- `Compressed JSON` (Long text)
- `Shortlist Status` (Single select: Pending, Shortlisted, Rejected)
- `LLM Summary` (Long text)
- `LLM Score` (Number)
- `LLM Follow-Ups` (Long text)

### 2. Personal Details (One-to-One with Applicants)
- `Applicant ID` (Link to Applicants)
- `Full Name`
- `Email`
- `Location`
- `LinkedIn`

### 3. Work Experience (One-to-Many with Applicants)
- `Applicant ID` (Link to Applicants)
- `Company`
- `Title`
- `Start Date`
- `End Date`
- `Technologies` (Multiple select)

### 4. Salary Preferences (One-to-One with Applicants)
- `Applicant ID` (Link to Applicants)
- `Preferred Rate`
- `Minimum Rate`
- `Currency`
- `Availability (hrs/wk)`

### 5. Shortlisted Leads (Helper Table)
- `Applicant ID` (Link to Applicants)
- `Compressed JSON` (Long text)
- `Score Reason` (Long text)
- `Created At` (Created time, auto)

🔗 Airtable Base Link: [View Airtable Base](https://airtable.com/)  

---

## 📝 User Input Flow

Since Airtable forms cannot write to multiple tables simultaneously:
- **Form 1:** Personal Details  
- **Form 2:** Work Experience  
- **Form 3:** Salary Preferences  

Each form requires `Applicant ID` and applicants must submit all three forms.

---

## 🐍 Python Automations

### Step 3: JSON Compression (`compress.py`)
- Fetches data from child tables.
- Builds a single JSON object per applicant.
- Writes it into `Applicants → Compressed JSON`.

### Step 4: JSON Decompression (`decompress.py`)
- Reads JSON from Applicants.
- Restores/upserts records into child tables.

### Step 5: Shortlist Automation (`shortlist.py`)
Rules for shortlisting:
- Experience ≥ 4 years OR worked at a Tier-1 company (Google, Meta, OpenAI, etc.).
- Preferred Rate ≤ $100/hr AND Availability ≥ 20 hrs/week.
- Location in {US, Canada, UK, Germany, India}.

If criteria met → Create entry in `Shortlisted Leads`.

### Step 6: LLM Evaluation (`llm_eval.py`)
- Triggered when `Compressed JSON` is updated.
- Calls an LLM (e.g., OpenAI GPT-4o-mini).
- Produces:
  - `LLM Summary` (≤ 75 words)
  - `LLM Score` (1–10)
  - `LLM Follow-Ups` (questions for clarification)

### Step 7: Combined Runner (`main.py`)
Runs the entire pipeline:
1. Compression  
2. Shortlisting  
3. LLM Evaluation  

```bash
python main.py
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-username/mercor-airtable-exercise.git
cd mercor-airtable-exercise
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure `.env`
Create a `.env` file in the project root:

```env
AIRTABLE_API_KEY=your_airtable_api_key
BASE_ID=your_airtable_base_id
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run Scripts
- Compress JSON:  
  ```bash
  python compress.py
  ```

- Decompress JSON:  
  ```bash
  python decompress.py
  ```

- Shortlist:  
  ```bash
  python shortlist.py
  ```

- LLM Evaluation:  
  ```bash
  python llm_eval.py
  ```

- Full pipeline:  
  ```bash
  python main.py
  ```

---

## 📊 Example: Compressed JSON

```json
{
  "personal": { "Full Name": "Jane Doe", "Location": "NYC" },
  "experience": [
    { "Company": "Google", "Title": "SWE" },
    { "Company": "Meta", "Title": "Engineer" }
  ],
  "salary": { "Preferred Rate": 100, "Currency": "USD", "Availability (hrs/wk)": 25 }
}
```

---

## ✅ Deliverables

1. Airtable Base (shared link) with tables, forms, and automations.  
2. Python scripts for compression, decompression, shortlisting, LLM enrichment.  
3. Documentation (this README.md).  

🔗 GitHub Repo: [https://github.com/your-username/mercor-airtable-exercise](https://github.com/your-username/mercor-airtable-exercise)  
🔗 Airtable Base: [https://airtable.com/](https://airtable.com/)  

---

## 🚀 Possible Extensions (Beyond Assignment)
- Automate experience calculation using exact Start/End dates.  
- Schedule pipeline with Cron or GitHub Actions.  
- Add error logging and dashboards in Airtable.  
- Support multiple LLM providers (Claude, Gemini, Azure OpenAI).  

---

## Author
**Vaibhav Rajendra Bhagwat**  
B.Tech IT, VJTI Mumbai  
