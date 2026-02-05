# 📦 Faculty Finder - Library Sizes

## Dependencies from requirements.txt

### Core Libraries

| Library | Version | Approximate Size | Purpose |
|---------|---------|-----------------|---------|
| **fastapi** | >=0.104.0 | ~5 MB | Web framework |
| **uvicorn[standard]** | >=0.24.0 | ~3 MB | ASGI server |
| **sentence-transformers** | >=2.2.0 | ~10 MB | AI model framework |
| **faiss-cpu** | >=1.7.4 | ~15 MB | Vector search engine |
| **numpy** | >=1.24.0 | ~25 MB | Numerical computing |
| **torch** | >=2.0.0 | **~800 MB** | PyTorch (AI backend) |
| **transformers** | >=4.30.0 | ~50 MB | Hugging Face transformers |

---

## Total Installed Size

**Base Libraries**: ~908 MB

**AI Model** (downloaded at runtime):
- Old model (`all-MiniLM-L6-v2`): ~420 MB
- **New model** (`paraphrase-MiniLM-L3-v2`): **~60 MB**

---

## Memory Usage Breakdown

### With Old Model (Failed on Render)
- Libraries: ~908 MB
- Model: ~420 MB
- Runtime overhead: ~100 MB
- **Total: ~1,428 MB** ❌ (Exceeded 512MB limit)

### With New Model (Should Work on Render)
- Libraries: ~908 MB (PyTorch is largest)
- Model: ~60 MB
- Runtime overhead: ~100 MB
- **Total: ~1,068 MB** ⚠️ (Still might be tight)

---

## Why PyTorch is So Large

**torch** (800MB) is the biggest dependency because:
- It's a full deep learning framework
- Includes CUDA support (even CPU version)
- Contains pre-compiled binaries

**Note**: `sentence-transformers` requires PyTorch, so we can't remove it.

---

## Optimization Options

### Option 1: Current Setup (Recommended)
- Use smaller model (60MB)
- Keep all libraries
- **May still exceed 512MB on Render free tier**

### Option 2: Minimal Setup (Not Recommended)
- Remove AI search entirely
- Use keyword search only
- Would reduce to ~50MB total
- **Defeats the purpose of semantic search**

### Option 3: Upgrade Render ($7/month)
- Get 512MB+ RAM
- Use original larger model
- Better search accuracy

---

## Data Files (Not in requirements.txt)

| File | Size | Purpose |
|------|------|---------|
| `faculty.index` | ~2-5 MB | FAISS vector index |
| `faculty_meta.json` | ~100-500 KB | Faculty metadata |
| `faculty.db` | ~500 KB - 2 MB | SQLite database |

---

## Recommendation

**For Render Free Tier:**
- The optimized setup might still be too large
- Consider using ngrok or Hugging Face Spaces instead
- Or upgrade to Render Starter ($7/month)

**For Development:**
- Current setup works perfectly on your local machine
- All features functional
