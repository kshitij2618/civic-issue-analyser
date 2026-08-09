from fastapi import FastAPI

app = FastAPI()


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "message": "FastAPI is working on Vercel"
    }


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "CiviSense backend is alive"
    }