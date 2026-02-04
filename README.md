# Deploying this FastAPI app to Railway

Steps to deploy your project to Railway (two common ways):

1) Deploy via GitHub (recommended)

- Commit and push the repository (including `faculty.index` and `faculty_meta.json`) to GitHub.
- In Railway dashboard, create a new project → "Deploy from GitHub" → connect the repo.
- Railway will detect `Procfile` and run the web command.

2) Deploy via Railway CLI

Install the Railway CLI, login, then run:

```bash
railway login
railway init   # follow prompts to create a project
railway up     # deploys the current folder
```

Notes:
- This project expects the data files `faculty.index` and `faculty_meta.json` to be present in the repository root so the app can load them at runtime.
- The app uses `sentence-transformers` which downloads model weights on first run; ensure the environment can reach the internet or pre-download weights if needed.
- Railway will provide a `PORT` environment variable; the `Procfile` uses it for `uvicorn`.
- If using the `Dockerfile`, you can push a container image instead of using the `Procfile`.

Useful commands locally:

```bash
# create virtualenv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# run locally (uvicorn will pick an available port)
uvicorn vector_api:app --reload
```
# 🎓 Faculty Finder – Data Pipeline Project

## 📌 Project Objective
The goal of this project is to build a complete data pipeline that collects, cleans, stores, and serves faculty information from a college website.  
The system is designed to support semantic search, where a student or researcher can type a natural language query like:

> “Who is working on sustainable energy and carbon capture?”

and retrieve relevant faculty members even if those exact keywords are not present in official titles.

This project focuses on:
- Scraping faculty data (names, bios, research interests)
- Cleaning and structuring the data
- Storing it in a relational database
- Making it ready for NLP and vector search applications

---
## 🧠 Project Lifecycle

### 1️⃣ Ingestion (Scraper)
- Crawls the college faculty directory
- Fetches HTML of individual faculty profile pages
- Extracts:x  x 
  - Name  
  - Biography  
  - Research Interests  
  - Specialization / Teaching / Publications (if available)

### 2️⃣ Transformation (Cleaner)
- Removes HTML tags and noisy text
- Handles:
  - Missing bios  
  - Encoding issues  
  - Special characters  
- Converts scraped output into clean structured JSON

### 3️⃣ Storage (Database)
- Uses SQLite (`faculty.db`)
- Stores cleaned data in structured tables
- Ensures persistence after script execution

### 4️⃣ Serving (Future Scope)
- API layer using FastAPI (planned)
- Endpoints like:
  - `/faculty/{id}`
  - `/all`

---
## 🧾 Dataset Schema

| Column | Description |
|--------|-------------|
| faculty_type | Category of faculty (regular, adjunct, etc.) |
| name | Full name of faculty member |
| education | Highest qualification |
| email | Official email address |
| specialization | Research and teaching areas |
| phone | Contact number (if available) |
| address | Office location |
---
FACULTY FINDER – USER MANUAL

1. Start the program.
2. Open your internet browser.
3. Type this link in the address bar:
   http://127.0.0.1:8000/docs
4. Press Enter.

5. To see all faculty:
   - Click /faculty
   - Click Try it out
   - Click Execute

6. To see faculty by type:
   - Click /faculty/type/
   - Click Try it out
   - Type:
     all        → see all faculty
     adjunct    → see adjunct faculty
     regular    → see regular faculty
   - Click Execute

7. To see one faculty by number:
   - Click /faculty/{faculty_id}
   - Click Try it out
   - Type a number (example: 1)
   - Click Execute

8. If nothing appears:
   - Refresh the page
   - Make sure the program is running

END
---
## 🧠 Faculty Specialization Distribution

The dataset includes faculty working across multiple research domains.  
Below is a specialization-wise distribution derived from the cleaned dataset:

| Specialization | Faculty Count |
|---------------|----------------|
| Machine Learning | 18 |
| Data Science | 12 |
| Computer Vision | 9 |
| Wireless Communications | 8 |
| Cybersecurity | 6 |
| Signal Processing | 5 |
| Networks | 5 |

*(Top specializations shown; faculty may belong to multiple categories.)*
---
## 📊 Domain-Level Summary

Specializations were grouped into broader domains for analytical usability:

| Domain | Faculty Count |
|--------|----------------|
| AI & ML | 28 |
| Data Science | 14 |
| Networking | 13 |
| Cybersecurity | 8 |
| Other | 46 |
Note: A single faculty member may be associated with multiple specializations; therefore, counts may exceed total faculty size.

---

## 📊 Dataset Statistics

- **Total faculty records:** 109  
- **Faculty categories:**
  - Regular: 67  
  - Adjunct: 26  
  - International Adjunct: 11  
  - Distinguished: 3  
  - Professor of Practice: 2  

- **Number of attributes per record:** 8  
  (`faculty_type, name, education, phone, address, email, specialization`)

- **Missing values (selected fields):**
  - Phone: 45 missing  
  - Address: 38 missing  
  - Email: 0 missing  

- **Data format:** JSON  
- **Database:** SQLite  
- **API:** FastAPI
---
## 🛠️ Technologies Used
- **Python 3.x**
- **Jupyter Notebook**
- **Libraries:**
  - requests  
  - BeautifulSoup  
  - pandas  
  - sqlite3  
  - json  

---
## 🔍 Example Analytical Questions

- How many faculty members work in AI & ML?
- Which specialization has the highest number of faculty?
- What is the distribution of faculty types?
- Can we cluster faculty by research domain?
- Which faculty have overlapping research areas?
---

## ⚠ Limitations

- Specialization is free-text and may contain semantic overlap (e.g., "AI" vs "Artificial Intelligence").
- A single faculty member may belong to multiple specializations.
- Some contact fields (phone, address) are missing for certain records.
- Data is scraped from public webpages and may change over time.
---
## 🚀 Future Scope

- Apply NLP to cluster faculty by research topics.
- Build a recommendation system for student–faculty matching.
- Integrate embeddings for semantic search.
- Periodically refresh dataset via scheduled scraping.
---

## 📂 Project Structure
```text
Faculty_project-/
│
├── main.py
│   → Runs the complete data pipeline: scraping faculty data, cleaning it,
│     and storing it into the SQLite database.
│
├── final.ipynb
│   → Notebook version of the full pipeline for step-by-step execution
│     and demonstration.
│
├── cleaning.ipynb
│   → Performs data cleaning and transformation on the raw scraped JSON
│     (removes HTML tags, handles nulls, fixes formatting).
│
├── json_to_sqlite.py
│   → Takes cleaned JSON data and inserts it into the SQLite database
│     using a defined schema.
│
├── check_db.py
│   → Utility script to verify database contents and check stored records.
│
├── faculty_raw.json
│   → Raw faculty data scraped directly from the website (uncleaned).
│
├── faculty_clean.json
│   → Cleaned and structured faculty data ready for database storage
│     and NLP tasks.
│
├── faculty.db
│   → SQLite database file storing structured faculty information.
│
├── Prompt_Log.txt
│   → Log of LLM prompts and responses used during the project.
│
└── README.md
    → Project documentation and usage instructions.

