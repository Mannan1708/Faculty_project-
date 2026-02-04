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

