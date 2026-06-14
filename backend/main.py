from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def root():
    return {"message": "Document Intelligence API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Just return file info for now
    return {
        "filename": file.filename,
        "size": file.size,
        "status": "received"
    }

@app.get("/health")
def health():
    return {"status": "alive"}
