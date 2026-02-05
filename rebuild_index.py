"""
Rebuild FAISS index with the correct model (all-MiniLM-L6-v2)
This ensures the index matches the model being used in vector_api.py
"""
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading the correct model: all-MiniLM-L6-v2...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading faculty metadata...")
with open("faculty_meta.json", "r") as f:
    metadata = json.load(f)

print(f"Processing {len(metadata)} faculty members...")
texts = []
for faculty in metadata:
    # Combine name and specialization for embedding
    text = f"{faculty['name']} {faculty['specialization']}"
    texts.append(text)

print("Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings, dtype=np.float32)

print(f"Creating FAISS index with {embeddings.shape[0]} vectors of dimension {embeddings.shape[1]}...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

print("Saving FAISS index...")
faiss.write_index(index, "faculty.index")

print(f"✅ Done! Rebuilt index for {len(metadata)} faculty members")
print(f"   Index dimension: {embeddings.shape[1]}")
print(f"   Total vectors: {index.ntotal}")
print("\nRestart your server to use the new index!")
