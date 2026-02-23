from fastapi import FastAPI

app = FastAPI(title="Medical API")

@app.get("/health")
def health():
    return {"status": "ok"}