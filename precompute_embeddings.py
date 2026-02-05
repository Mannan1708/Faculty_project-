"""
Pre-compute embeddings for all faculty members.
Run this LOCALLY before deploying to generate faculty_embeddings.json

This script requires sentence-transformers to be installed locally.
It will NOT be needed in production.
"""

from sentence_transformers import SentenceTransformer
import json
import numpy as np

print("Loading SentenceTransformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading faculty metadata...")
with open("faculty_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

print(f"Generating embeddings for {len(metadata)} faculty members...")
embeddings = []
for i, fac in enumerate(metadata):
    # Create text representation for embedding
    text = f"{fac['name']} {fac['specialization']}"
    embedding = model.encode(text)
    embeddings.append(embedding.tolist())
    
    if (i + 1) % 10 == 0:
        print(f"  Processed {i + 1}/{len(metadata)} faculty members...")

# Save embeddings
print("Saving embeddings to faculty_embeddings.json...")
with open("faculty_embeddings.json", "w") as f:
    json.dump(embeddings, f)

print(f"✓ Successfully generated {len(embeddings)} embeddings")
print(f"✓ Saved to faculty_embeddings.json")
print("\nYou can now deploy the application without sentence-transformers!")
