from fastapi import APIRouter, HTTPException,UploadFile, File,Form
from typing import Dict
import os
import uuid
from practice.Controler.interview_controler import InterviewController, Event
from practice.Controler.Ai_engine import AIEngine
from api.interview_ws import create_session
from api.interview_ws import get_session

router = APIRouter(prefix="/tech_round", tags=["Tech Round"])

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@router.post("/start")
async def start_tech(
    role: str = Form(...),
    experience: str = Form(...),
    difficulty: str = Form("medium"),
    personality: str = Form("friendly"),
    mode: str = Form("voice"),
    resume: UploadFile = File(None)
):

    # ---------- Save resume ----------
    resume_path = None

    try:
        if not role or not experience:
            raise HTTPException(
        status_code=400,
        detail="role and experience are required"
        )
        if resume:
            print("resume received")
            file_id = str(uuid.uuid4())
            resume_path = f"{UPLOAD_DIR}/{file_id}_{resume.filename}"
            
            with open(resume_path, "wb") as f:
                f.write(await resume.read())
        # Initialize engines
        ai_engine = AIEngine(mode="TECH")
    
        # Create controller
        controller = InterviewController(ai_engine=ai_engine)
    
        # Create session
        session_id = create_session(controller)
    
        # Start interview
        response = await controller.handle_event(
            Event.START_INTERVIEW,
            {
                "role": role,
                "experience": experience,
                "difficulty": difficulty,
                "personality": personality,
                "resume_path": resume_path,
                "mode": mode
            }
        )
        print("START RESPONSE:", response)
        return {
            "message": "Tech interview started",
            "session_id": session_id,
            "response": response
            # "question": response.get("question")
        }
    
    except Exception as e:
        raise HTTPException(
        status_code=500,
        detail=f"Failed to start interview: {str(e)}"
    )
        
        

@router.post("/answer")
async def answer(payload: Dict):

    session_id = payload.get("session_id")
    answer = payload.get("answer")

    controller = get_session(session_id)

    if not controller:
        raise HTTPException(status_code=404, detail="Session not found")

    response = await controller.handle_event(
        Event.USER_FINISHED_SPEAKING,
        {"answer": answer}
    )

    return response

@router.post("/end")
async def end_interview(payload: Dict):

    session_id = payload.get("session_id")

    controller = get_session(session_id)

    response = await controller.handle_event(Event.END_INTERVIEW)

    return response



