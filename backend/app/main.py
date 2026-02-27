from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException

app = FastAPI(title="Medical API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
def upload(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(400,detail="invalida document type")
    else:
        data = file.file.read()
    return {"filename": file.filename}