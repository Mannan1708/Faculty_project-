import uvicorn
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print("Starting Faculty Finder AI Engine...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
