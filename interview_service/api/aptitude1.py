from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from typing import Literal, Optional
from practice.Aptitude.engines import session_engine, role_engine
from practice.Aptitude.formula_engine.topic_map import TOPIC_MAP
from practice.Aptitude.concepts.topic_concepts import ALL_CONCEPTS

router = APIRouter()

ENGINES = {
    "session": session_engine,
    "role": role_engine,
}


@router.post("/generate-questions")
async def generate_questions(
    engine: Literal["session", "role"] = Form(...),
    topic: str = Form(...),
    difficulty: Literal["easy", "medium", "hard"] = Form(...),
    count: int = Form(..., ge=1, le=50),
    user_id: str = Form(default="admin"),
      # ready for future use
):
    selected_engine = ENGINES.get(engine)
    if not selected_engine:
        raise HTTPException(status_code=400, detail=f"Unknown engine: {engine}")

    try:
        result = await selected_engine.run(
            topic=topic,
            difficulty=difficulty,
            count=count,
            user_id=user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")
    
    return {
    "status": "done",
    "engine": engine,
    "topic": topic,
    "difficulty": difficulty,
    "requested": count,
    **result,
    }


@router.get("/topics")
async def list_topics():
    return {
"session": {
    aptitude: list(topics.keys())
    for aptitude, topics in ALL_CONCEPTS.items()
},
"role": list(TOPIC_MAP.keys()),
}
