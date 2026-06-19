from fastapi import FastAPI
from api import Tech, Hr, aptitude1, aptitude
from fastapi.middleware.cors import CORSMiddleware  
from api.interview_ws import router as interview_router

app = FastAPI(title="Interview Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Tech.router)
app.include_router(Hr.router)
app.include_router(aptitude.router)
app.include_router(aptitude1.router)
app.include_router(interview_router)

@app.get("/health")
async def health():
    return {"status":"ok"}                                                                                  
# import os

# port = int(os.environ.get("PORT", 10000))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=port)
