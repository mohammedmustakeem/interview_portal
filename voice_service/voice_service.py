import base64
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import edge_tts
import os

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


class VoiceEngine:
    def __init__(self):
        # session_id -> audio buffer
        self.audio_buffers = {}
        self.processing_flags = {}

       
    # Receive audio chunk per session
    async def receive_audio_chunk(self, session_id: str, chunk: bytes):
        if session_id not in self.audio_buffers:
            self.audio_buffers[session_id] = bytearray()

        self.audio_buffers[session_id].extend(chunk)

     
    # Process speech (STT)
    async def process_speech(self, session_id: str):
        if self.processing_flags.get(session_id, False):
            return None

        self.processing_flags[session_id] = True

        try:
            buffer = self.audio_buffers.get(session_id)

            if not buffer or len(buffer) == 0:
                return None

            audio_bytes = bytes(buffer)
            self.audio_buffers[session_id] = bytearray()

            #  Non-blocking STT call
            transcript = await asyncio.to_thread(
                client.audio.transcriptions.create,
                model="whisper-1",
                file=("audio.webm", audio_bytes, "audio/webm")
            )

            user_text = transcript.text
            print(f" Whisper transcript: '{user_text}'")
            return {
            "type": "USER_TEXT",
            "session_id": session_id,
            "text": user_text
        }

        finally:
            self.processing_flags[session_id] = False

            # -------------------------------
            # TTS (Text to Speech)
            # -------------------------------
    async def speak(self, text: str):
        print("Entering speak()")
        if not text:
            return None

        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-JennyNeural"
        )
        audio_buffer = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.extend(chunk["data"])
        audio_base64 = base64.b64encode(bytes(audio_buffer)).decode("utf-8")
        print("Audio saved as output.mp3")

        # audio_buffer = bytearray()

        # async for chunk in communicate.stream():
        #     if chunk["type"] == "audio":
        #         audio_buffer.extend(chunk["data"])
        print("Exiting speak()")
        return {
              "type": "AI_RESPONSE",
                "text": text,
                "format": "mp3",
                "audio": audio_base64
        }    
        
