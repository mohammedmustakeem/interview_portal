# vision_service/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vision import router as vision_router
import os

app = FastAPI(title="Synclyft Vision Service")

# Allow frontend / interview service to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vision_router,prefix="/vision")


@app.get("/health")
async def health():
    return {"status": "vision service running"}


# Required for Render / Railway
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)
