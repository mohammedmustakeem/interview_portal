from typing import Dict
from practice.Controler.interview_controler import InterviewController
from practice.Controler.Ai_engine import AIEngine
from api.interview_ws import create_session
from fastapi import APIRouter, HTTPException,UploadFile, File,Form

router = APIRouter(prefix="/hr", tags=["HR Round"])


@router.post("/start")
async def start_hr(
    role: str = Form(...),
    experience: str = Form(...),
    resume: UploadFile = File(None)
):
    ai_engine = AIEngine(mode="HR")

    controller = InterviewController(ai_engine=ai_engine)

    session_id = create_session(controller)

    # Immediately start AI with role & experience
    first_question = await ai_engine.start(role, experience,resume)

    return {
        "message": "HR interview initialized",
        "session_id": session_id,
        "first_question" : first_question
    }
