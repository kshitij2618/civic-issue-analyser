from fastapi import FastAPI

app = FastAPI(
    title="CiviSense AI",
    version="1.0.0"
)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "message": "CiviSense backend is working"
    }