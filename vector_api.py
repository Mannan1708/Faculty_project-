from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import faiss
import json
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Faculty Semantic Search")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("faculty.index")

# Load metadata
with open("faculty_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Faculty Semantic Search</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #f5f7fa, #c3cfe2);
                margin: 0;
                padding: 0;
            }
            .container {
                width: 80%;
                margin: auto;
                margin-top: 50px;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .search-box {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }
            input {
                width: 70%;
                padding: 10px;
                font-size: 16px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            button {
                padding: 10px 20px;
                margin-left: 10px;
                border: none;
                border-radius: 8px;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .footer {
                text-align: center;
                margin-top: 15px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Faculty Semantic Search</h1>

            <div class="search-box">
                <input type="text" id="query" placeholder="e.g. machine learning and computer vision">
                <button onclick="search()">Search</button>
            </div>

            <div id="results"></div>

            <div class="footer">
                Semantic search over faculty profiles using embeddings
            </div>
        </div>

        <script>
            async function search() {
                const query = document.getElementById("query").value;
                if (!query) return;

                const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
                const data = await response.json();

                let html = "<table><tr><th>Rank</th><th>Name</th><th>Faculty Type</th><th>Specialization</th><th>Similarity</th></tr>";

                data.results.forEach(r => {
                    html += `<tr>
                        <td>${r.rank}</td>
                        <td>${r.name}</td>
                        <td>${r.faculty_type}</td>
                        <td>${r.specialization}</td>
                        <td>${r.similarity}</td>
                    </tr>`;
                });

                html += "</table>";
                document.getElementById("results").innerHTML = html;
            }
        </script>
    </body>
    </html>
    """

# ---------------- API SEARCH ----------------
@app.get("/api/search")
def api_search(query: str = Query(...), top_k: int = 5):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, top_k)

    results = []
    for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
        faculty = metadata[idx]
        similarity = 1 / (1 + dist)

        spec = faculty["specialization"]
        if len(spec) > 120:
            spec = spec[:120] + "..."

        results.append({
            "rank": rank,
            "name": faculty["name"],
            "faculty_type": faculty["faculty_type"],
            "specialization": spec,
            "similarity": round(similarity, 3)
        })

    return {"query": query, "results": results}
