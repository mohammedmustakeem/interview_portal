from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
from voice_service import VoiceEngine
import base64
app = FastAPI()

#  CORS middleware FIRST - before any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

voice_engine = VoiceEngine()

#Define Pydantic model
class TTSRequest(BaseModel):
    text: str

    # REST endpoint - /speak
@app.post("/speak")
async def speak_api(req: TTSRequest):
    """Text-to-Speech endpoint"""
    result = await voice_engine.speak(req.text)
    return result

@app.websocket("/ws/audio/{session_id}")
async def websocket_audio(ws: WebSocket, session_id: str):
    await ws.accept()
    print(f" Connected: {session_id}")
    try:
        while True:
            data = await ws.receive()

            if "bytes" in data:
                chunk = data["bytes"]
                print(f"📦 Received binary chunk: {len(chunk)} bytes")
                await voice_engine.receive_audio_chunk(session_id, chunk)

            elif "text" in data:
                message = data["text"]
                print(f"📨 Received text message: {message}")

                if message == "STOP":
                    print(f"🛑 STOP received for {session_id}, processing...")
                    result = await voice_engine.process_speech(session_id)
                    print(f"🎙️ STT result: {result}")

                    if result:
                        await ws.send_json(result)
                        print(f"✅ Sent USER_TEXT back to frontend")
                    else:
                        # Tell frontend something went wrong
                        await ws.send_json({
                            "type": "USER_TEXT",
                            "session_id": session_id,
                            "text": "",
                            "error": "No audio received or transcription failed"
                        })
                        print("⚠️ No result from process_speech")
                else:
                    audio_bytes = base64.b64decode(message)
                    print(f"📦 Received base64 chunk decoded: {len(audio_bytes)} bytes")
                    await voice_engine.receive_audio_chunk(session_id, audio_bytes)

    except WebSocketDisconnect:
        print(f"❌ Disconnected: {session_id}")
    except Exception as e:
        print(f"💥 Error: {e}")
        
        
        
@app.get("/")
async def root():
        return {"status": "Voice Service is running", "endpoints": ["/speak", "/ws/audio/{session_id}"]}

@app.get("/health")
async def health():
    return {"status": "healthy"}

    #  Run server
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
