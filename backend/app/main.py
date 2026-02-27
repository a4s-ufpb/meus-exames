from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(title="Medical API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
 
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid document type. Send a PDF.")

  
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file extension. File must end with .pdf")

    data = await file.read()


    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="File does not look like a valid PDF.")

    return {"filename": file.filename, "bytes": len(data)}