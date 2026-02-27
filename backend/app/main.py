from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException

app = FastAPI(title="Medical API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
def upload(file: UploadFile):
    data = file.file.read()
    return {"filename": file.filename}