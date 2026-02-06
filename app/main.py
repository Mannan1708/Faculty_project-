from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os

from . import crud, schemas
from .recommender import recommender

app = FastAPI(title="Faculty Finder API", version="2.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Faculty Finder AI Engine is Running", "docs": "/docs", "dashboard": "/static/index.html"}

@app.get("/faculty", response_model=List[schemas.Faculty])
async def read_faculties(skip: int = 0, limit: int = 20):
    return crud.get_all_faculty(skip=skip, limit=limit)

@app.get("/faculty/search", response_model=List[schemas.FacultyRecommendation])
async def search_faculties(q: str = Query(..., min_length=2)):
    """
    Hybrid Global Search:
    1. Exact Match: SQL 'LIKE' query to find names, emails, or specific attributes.
    2. AI Match: Vector Engine to find semantic/topic matches.
    Merges both for the best experience.
    """
    # 1. Exact/SQL Search
    exact_matches = crud.search_faculty(q)
    
    # Enrich exact matches to match the Recommendation Schema
    processed_exact = []
    seen_ids = set()
    for item in exact_matches:
        # Clone to avoid mutating if it's a shared reference (unlikely here but safe)
        match = item.copy()
        match['similarity_score'] = 1.0
        match['recommendation_type'] = "Direct Match"
        match['matched_keywords'] = ["Name/Attribute Match"]
        
        processed_exact.append(match)
        seen_ids.add(match['id'])

    # 2. AI Search
    ai_matches = recommender.get_subject_specialty_match(q, top_n=20)
    
    # 3. Merge (AI results that aren't already in Exact)
    final_results = processed_exact
    for item in ai_matches:
        if item['id'] not in seen_ids:
            final_results.append(item)
            
    return final_results

@app.get("/faculty/{faculty_id}", response_model=schemas.Faculty)
async def read_faculty(faculty_id: int):
    faculty = crud.get_faculty(faculty_id)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty

# --- Recommendation Endpoints ---

@app.get("/faculty/{faculty_id}/expertise", response_model=List[schemas.FacultyRecommendation])
async def get_expertise_matches(faculty_id: int, top_n: int = 5):
    """IDEA 1: Semantic Expertise Matcher"""
    results = recommender.get_semantic_expertise(faculty_id, top_n)
    return results

@app.get("/faculty/{faculty_id}/collaborators", response_model=List[schemas.FacultyRecommendation])
async def get_collaborators(faculty_id: int, top_n: int = 5):
    """IDEA 2: Multidisciplinary Bridge"""
    results = recommender.get_multidisciplinary_bridge(faculty_id, top_n)
    return results

@app.get("/recommend/subject", response_model=List[schemas.FacultyRecommendation])
async def match_subject(query: str = Query(..., min_length=3), top_n: int = 5):
    """IDEA 3: Subject-Specialty Matcher (Student Goal Alignment)"""
    results = recommender.get_subject_specialty_match(query, top_n)
    return results

# Static files for UI
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
