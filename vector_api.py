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
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #fff;
                padding: 40px 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 60px; animation: fadeIn 0.8s; }
            .logo { font-size: 3.5rem; font-weight: 800; margin-bottom: 10px; }
            .tagline { font-size: 1.2rem; opacity: 0.9; }
            .search-section {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                padding: 50px;
                margin-bottom: 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .search-box { display: flex; gap: 15px; margin-bottom: 20px; }
            input {
                flex: 1;
                padding: 18px 20px;
                font-size: 1.05rem;
                border-radius: 16px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.15);
                color: #fff;
                font-family: 'Inter', sans-serif;
            }
            input::placeholder { color: rgba(255, 255, 255, 0.6); }
            button {
                padding: 18px 40px;
                border: none;
                border-radius: 16px;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                font-size: 1.05rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            button:hover { transform: translateY(-2px); }
            .result-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s;
            }
            .result-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.15); }
            .result-name { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; }
            .meta-badge {
                display: inline-block;
                padding: 6px 14px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                font-size: 0.85rem;
                margin-right: 10px;
            }
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎓 Faculty Finder</div>
                <div class="tagline">AI-Powered Semantic Search</div>
            </div>
            <div class="search-section">
                <div class="search-box">
                    <input type="text" id="query" placeholder="Search by research interests, expertise, or topic...">
                    <button onclick="search()">Search</button>
                </div>
            </div>
            <div id="results"></div>
        </div>
        <script>
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
                        html += `
                            <div class="result-card">
                                <div class="result-name">${r.rank}. ${r.name}</div>
                                <div style="margin-bottom:15px;">
                                    <span class="meta-badge">📚 ${r.faculty_type}</span>
                                    <span class="meta-badge">✨ ${(r.similarity * 100).toFixed(1)}% Match</span>
                                </div>
                                <div><strong>Specialization:</strong> ${r.specialization}</div>
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
