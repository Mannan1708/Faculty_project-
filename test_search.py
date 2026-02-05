from sentence_transformers import SentenceTransformer
import faiss
import json

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded!")

print("Loading FAISS index...")
index = faiss.read_index("faculty.index")
print(f"Index loaded! Dimension: {index.d}, Total vectors: {index.ntotal}")

print("Loading metadata...")
with open("faculty_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)
print(f"Metadata loaded! Total faculty: {len(metadata)}")

print("\nTesting search...")
query = "machine learning"
query_vec = model.encode([query]).astype("float32")
distances, indices = index.search(query_vec, 3)

print(f"\nTop 3 results for '{query}':")
for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
    faculty = metadata[idx]
    similarity = 1 / (1 + dist)
    print(f"{rank}. {faculty['name']} - {similarity:.3f} similarity")
    print(f"   Type: {faculty['faculty_type']}")
    print(f"   Spec: {faculty['specialization'][:100]}...")
    print()

print("Test completed successfully!")
