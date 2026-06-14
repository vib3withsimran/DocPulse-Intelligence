import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import DocumentParser

app = FastAPI(
    title="Document Intelligence API",
    description="Backend API for Document Ingestion, Parsing, Classification, and RAG Chatbot.",
    version="1.0.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "storage")
os.makedirs(UPLOAD_DIR, exist_ok=True)

parser = DocumentParser()

@app.get("/")
def root():
    return {"message": "Document Intelligence API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Basic security check to avoid path traversal
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        # Save file securely in chunks to prevent memory bloat
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse the saved document
        parsed_data = parser.parse(file_path, safe_filename)
        
        return {
            "filename": safe_filename,
            "size": file.size,
            "status": "success",
            "data": parsed_data
        }
    except Exception as e:
        # Cleanup file if save/parse failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.get("/health")
def health():
    return {"status": "alive"}

