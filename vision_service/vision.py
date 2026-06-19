import traceback
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from detection import VisionService

router = APIRouter(tags=["Vision"])

ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5500",
    "null",
]
# ── Per-connection registry ────────────────────────────────────────────────────
# Stores active vision service per websocket client_id so recalibrate can reach it
_active_services: dict[str, VisionService] = {}


@router.websocket("/ws")
async def vision_ws(websocket: WebSocket):
    origin = websocket.headers.get("origin", "")

    # Allow all localhost origins for dev
    is_allowed = (
        origin in ALLOWED_ORIGINS
        or origin.startswith("http://localhost")
        or origin.startswith("http://127.0.0.1")
        or origin == "null"
        or origin == "" 
    )
    if not is_allowed:
        await websocket.close(code=1008)
        print(f" Rejected origin: {origin}")
        return

    await websocket.accept()

    # Unique key per connection
    client_id = f"{websocket.client.host}:{websocket.client.port}"
    print(f" Vision socket connected [{client_id}]")

    vision_service = VisionService()
    _active_services[client_id] = vision_service

    try:
        while True:
            data = await websocket.receive_json()

            # ── Recalibrate command via websocket ──────────────────────────
            if data.get("command") == "recalibrate":
                vision_service.recalibrate()
                await websocket.send_json({"status": "recalibrating"})
                continue

            base64_frame = data.get("frame")
            phase        = data.get("phase", "USER_SPEAKING")

            if not base64_frame:
                await websocket.send_json({"phase": phase, "warnings": []})
                continue

            result = await vision_service.process_frame_async(base64_frame, phase)

            if not isinstance(result, dict):
                result = {"phase": phase, "warnings": []}

            await websocket.send_json(result)

    except WebSocketDisconnect:
        print(f" Vision client disconnected [{client_id}]")

    except Exception as e:
        print(f" Vision WS error [{client_id}]:", e)
        traceback.print_exc()
        try:
            await websocket.send_json({
                "phase": "ERROR",
                "warnings": ["Vision processing error"]
            })
        except Exception:
            pass

    finally:
        # Clean up registry on disconnect
        _active_services.pop(client_id, None)
        print(f" Vision WS closed [{client_id}]")


        # ── HTTP recalibrate (optional — if you want a button in your UI) ─────────────
@router.post("/recalibrate/{client_id}")
async def recalibrate(client_id: str):
    service = _active_services.get(client_id)
    if not service:
        return {"status": "error", "detail": f"No active session for {client_id}"}
    service.recalibrate()
    return {"status": "recalibrating", "client_id": client_id}
