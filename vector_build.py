import json
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# 1. Load cleaned data
with open("faculty_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 2. Create text field for embeddings
df["bio_text"] = (
    df["name"].fillna("") + ". " +
    df["specialization"].fillna("") + ". " +
    df["biography"].fillna("") + ". " +
    df["education"].fillna("")
)

# 3. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Generate embeddings
embeddings = model.encode(df["bio_text"].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# 5. Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# 6. Save FAISS index
faiss.write_index(index, "faculty.index")

# 7. Save metadata (to map results)
df[["name", "faculty_type", "specialization"]].to_json(
    "faculty_meta.json",
    orient="records",
    indent=2
)

print("✅ FAISS index created")
print("Total vectors:", index.ntotal)
