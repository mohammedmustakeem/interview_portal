from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import uuid

from practice.Controler.interview_controler import Event
from practice.Controler.Ai_engine import AIEngine
from practice.Controler.interview_controler import InterviewController

router = APIRouter(prefix="/interview", tags=["Interview"])

# In-memory session store (later replace with Redis)
sessions = {}


# 
def create_session(controller):
    session_id = str(uuid.uuid4())
    sessions[session_id] = controller
    return session_id


def get_session(session_id):
    return sessions.get(session_id)


def delete_session(session_id):
    sessions.pop(session_id, None)


# WebSocket Endpoint

@router.websocket("/ws/{session_id}")
async def interview_ws(websocket: WebSocket, session_id: str):

    await websocket.accept()

    controller = get_session(session_id)

    if not controller:
        await websocket.close()
        return

    try:
        while True:
            data = await websocket.receive_json()

            event = data.get("type")
            payload = data.get("payload", {})

            result = await controller.handle_event(event, payload)

            if result:
                await websocket.send_json(result)

    except Exception:
        pass

    finally:
        delete_session(session_id)
        await websocket.close()
