from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Faculty Semantic Search")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and data
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Loading FAISS index...")
index = faiss.read_index("faculty.index")
print("Loading metadata...")
with open("faculty_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)
print(f"Ready! {len(metadata)} faculty members loaded.")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Faculty Finder - AI Search</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0a1929 0%, #1a2332 50%, #0d1b2a 100%);
                min-height: 100vh;
                color: #ffffff;
                padding: 40px 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 60px; animation: fadeIn 0.8s; }
            .logo { 
                font-size: 3.5rem; 
                font-weight: 800; 
                margin-bottom: 10px;
                background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .tagline { font-size: 1.2rem; color: #ffffff; letter-spacing: 1px; }
            .search-section {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                padding: 50px;
                margin-bottom: 40px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(66, 165, 245, 0.2);
            }
            .search-box { display: flex; gap: 15px; margin-bottom: 20px; }
            input {
                flex: 1;
                padding: 18px 24px;
                font-size: 1.05rem;
                border-radius: 16px;
                border: 2px solid rgba(66, 165, 245, 0.3);
                background: rgba(255, 255, 255, 0.05);
                color: #e3f2fd;
                font-family: 'Inter', sans-serif;
                transition: all 0.3s;
            }
            input:focus {
                outline: none;
                border-color: #42a5f5;
                background: rgba(255, 255, 255, 0.08);
                box-shadow: 0 0 0 3px rgba(66, 165, 245, 0.1);
            }
            input::placeholder { color: rgba(144, 202, 249, 0.5); }
            button {
                padding: 18px 45px;
                border: none;
                border-radius: 16px;
                background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
                color: white;
                font-size: 1.05rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 8px 20px rgba(25, 118, 210, 0.4);
            }
            button:hover { 
                transform: translateY(-3px); 
                box-shadow: 0 12px 30px rgba(25, 118, 210, 0.5);
                background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
            }
            .result-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                padding: 35px;
                margin-bottom: 24px;
                border: 1px solid rgba(66, 165, 245, 0.2);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }
            .result-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
                opacity: 0;
                transition: opacity 0.3s;
            }
            .result-card:hover::before { opacity: 1; }
            .result-card:hover { 
                transform: translateY(-8px); 
                border-color: rgba(66, 165, 245, 0.4);
                background: rgba(255, 255, 255, 0.08);
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            }
            .rank-badge {
                position: absolute;
                top: 20px;
                right: 20px;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
                color: #fff;
                font-size: 1.3rem;
                font-weight: 800;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 15px rgba(25, 118, 210, 0.5);
            }
            .rank-badge.top-3 {
                background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
                color: #1a2332;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            .result-header {
                display: flex;
                align-items: flex-start;
                margin-bottom: 16px;
                padding-right: 60px;
            }
            .result-name { 
                font-size: 1.6rem; 
                font-weight: 700; 
                line-height: 1.3;
                color: #ffffff;
            }
            .meta-row {
                display: flex;
                gap: 12px;
                margin-bottom: 16px;
                flex-wrap: wrap;
            }
            .meta-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 8px 16px;
                background: rgba(66, 165, 245, 0.15);
                border: 1px solid rgba(66, 165, 245, 0.3);
                border-radius: 12px;
                font-size: 0.9rem;
                font-weight: 500;
                color: #ffffff;
            }
            .similarity-badge {
                background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
                color: #fff;
                font-weight: 700;
                padding: 8px 18px;
                box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
                border: none;
            }
            .similarity-badge.high { background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%); }
            .similarity-badge.medium { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
            .similarity-badge.low { background: linear-gradient(135deg, #757575 0%, #616161 100%); }
            .spec-text {
                color: #ffffff;
                line-height: 1.6;
                font-size: 1rem;
            }
            .spec-label {
                color: #ffffff;
                font-weight: 600;
                margin-right: 8px;
            }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
            .result-card { animation: fadeIn 0.5s ease-out; }
            .info-section {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                padding: 20px 30px;
                margin-bottom: 30px;
                border: 1px solid rgba(66, 165, 245, 0.2);
                text-align: center;
            }
            .info-section h3 {
                color: #ffffff;
                font-size: 0.95rem;
                font-weight: 600;
                margin-bottom: 12px;
            }
            .faculty-types {
                display: flex;
                gap: 10px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .faculty-type-badge {
                padding: 6px 14px;
                background: rgba(66, 165, 245, 0.15);
                border: 1px solid rgba(66, 165, 245, 0.3);
                border-radius: 8px;
                font-size: 0.85rem;
                color: #ffffff;
                font-weight: 500;
            }
            .suggestions {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 15px;
                justify-content: center;
            }
            .suggestion-tag {
                padding: 8px 16px;
                background: rgba(66, 165, 245, 0.2);
                border: 1px solid rgba(66, 165, 245, 0.4);
                border-radius: 20px;
                font-size: 0.9rem;
                color: #ffffff;
                cursor: pointer;
                transition: all 0.3s;
            }
            .suggestion-tag:hover {
                background: rgba(66, 165, 245, 0.35);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(66, 165, 245, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎓 Faculty Finder</div>
                <div class="tagline">Dhirubhai Ambani University (DAU)</div>
            </div>
            <div class="info-section">
                <h3>Search across all faculty types:</h3>
                <div class="faculty-types">
                    <span class="faculty-type-badge">Regular</span>
                    <span class="faculty-type-badge">Adjunct</span>
                    <span class="faculty-type-badge">International Adjunct</span>
                    <span class="faculty-type-badge">Professor of Practice</span>
                    <span class="faculty-type-badge">Distinguished</span>
                </div>
            </div>
            <div class="search-section">
                <div class="search-box">
                    <input type="text" id="query" placeholder="Search by research interests, expertise, or topic...">
                    <button onclick="search()">Search</button>
                </div>
                <div class="suggestions">
                    <span class="suggestion-tag" onclick="quickSearch('machine learning')">🤖 Machine Learning</span>
                    <span class="suggestion-tag" onclick="quickSearch('artificial intelligence')">🧠 AI</span>
                    <span class="suggestion-tag" onclick="quickSearch('data science')">📊 Data Science</span>
                    <span class="suggestion-tag" onclick="quickSearch('computer vision')">👁️ Computer Vision</span>
                    <span class="suggestion-tag" onclick="quickSearch('natural language processing')">💬 NLP</span>
                    <span class="suggestion-tag" onclick="quickSearch('blockchain')">⛓️ Blockchain</span>
                    <span class="suggestion-tag" onclick="quickSearch('cybersecurity')">🔒 Cybersecurity</span>
                </div>
            </div>
            <div id="results"></div>
        </div>
        <script>
            function quickSearch(query) {
                document.getElementById('query').value = query;
                search();
            }
            
            async function search() {
                const query = document.getElementById('query').value.trim();
                if (!query) return;
                
                document.getElementById('results').innerHTML = '<div style="text-align:center;padding:40px;">Searching...</div>';
                
                try {
                    const response = await fetch(`/api/search?query=${encodeURIComponent(query)}&top_k=10`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    if (!data.results || data.results.length === 0) {
                        document.getElementById('results').innerHTML = '<div style="text-align:center;padding:40px;">No results found. Try different keywords.</div>';
                        return;
                    }
                    
                    let html = '';
                    data.results.forEach(r => {
                        // Determine similarity badge class
                        const simPercent = r.similarity * 100;
                        let simClass = 'similarity-badge';
                        if (simPercent >= 70) simClass += ' high';
                        else if (simPercent >= 50) simClass += ' medium';
                        else simClass += ' low';
                        
                        // Top 3 get special badge animation
                        const rankClass = r.rank <= 3 ? 'rank-badge top-3' : 'rank-badge';
                        
                        html += `
                            <div class="result-card">
                                <div class="${rankClass}">#${r.rank}</div>
                                <div class="result-header">
                                    <div class="result-name">${r.name}</div>
                                </div>
                                <div class="meta-row">
                                    <span class="meta-badge">📚 ${r.faculty_type}</span>
                                    <span class="${simClass}">✨ ${simPercent.toFixed(1)}% Match</span>
                                </div>
                                <div class="spec-text">
                                    <span class="spec-label">Specialization:</span>${r.specialization}
                                </div>
                            </div>
                        `;
                    });
                    document.getElementById('results').innerHTML = html;
                } catch (error) {
                    console.error('Search error:', error);
                    document.getElementById('results').innerHTML = `
                        <div style="text-align:center;padding:40px;background:rgba(255,0,0,0.1);border-radius:16px;">
                            <h3 style="color:#ff6b6b;margin-bottom:10px;">⚠️ Error Processing Request</h3>
                            <p><strong>Details:</strong> ${error.message}</p>
                            <p style="margin-top:10px;font-size:0.9rem;opacity:0.8;">Check browser console (F12) for more details</p>
                        </div>
                    `;
                }
            }
            document.getElementById('query').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') search();
            });
        </script>
    </body>
    </html>
    """

@app.get("/api/search")
def search(query: str, top_k: int = 5):
    # Encode query
    query_embedding = model.encode([query])
    query_vec = np.array(query_embedding, dtype=np.float32)
    
    # Search
    distances, indices = index.search(query_vec, top_k)
    
    # Build results
    results = []
    for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
        fac = metadata[int(idx)]
        similarity = 1 / (1 + float(dist))
        spec = fac["specialization"]
        if len(spec) > 120:
            spec = spec[:120] + "..."
        
        results.append({
            "rank": rank,
            "name": fac["name"],
            "faculty_type": fac["faculty_type"],
            "specialization": spec,
            "similarity": float(similarity)
        })
    
    return {"query": query, "results": results}
