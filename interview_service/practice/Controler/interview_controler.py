import asyncio
from enum import Enum
import json
from practice.Controler.Ai_engine import AIEngine


class Phase(str, Enum):
    GREETING = "GREETING"
    IDLE = "IDLE"
    AI_SPEAKING = "AI_SPEAKING"
    USER_SPEAKING = "USER_SPEAKING"
    PROCESSING = "PROCESSING"
    FINALIZING = "FINALIZING"


class Event(str, Enum):
    START_INTERVIEW = "START_INTERVIEW"
    USER_FINISHED_SPEAKING = "USER_FINISHED_SPEAKING"
    USER_STARTED_SPEAKING = "USER_STARTED_SPEAKING"
    END_INTERVIEW = "END_INTERVIEW"


class InterviewController:

    def __init__(self, ai_engine):
        self.phase = Phase.IDLE
        self.ai_engine = ai_engine
        self.current_question = None
        self.lock = asyncio.Lock()
       
        
    async def handle_event(self, event: Event, payload=None):

        async with self.lock:

            if event == Event.START_INTERVIEW:
                return await self._start_interview(payload)

            elif event == Event.USER_STARTED_SPEAKING:
                await self._handle_interrupt()
                return {"phase": self.phase.value}

            elif event == Event.USER_FINISHED_SPEAKING:
                answer = payload.get("answer")
                return await self._process_user_answer(answer)

            elif event == Event.END_INTERVIEW:
                return await self._finalize_interview()
                #return {"phase": self.phase.value}

        return {"phase": self.phase.value}

    async def _start_interview(self, payload):
        
        self._set_phase(Phase.PROCESSING)
        role = payload.get("role")
        experience = payload.get("experience")
        difficulty = payload.get("difficulty")
        personality = payload.get("personality")
        resume_path = payload.get("resume_path")
    
        first_question = await self.ai_engine.start(
            role=role,
            experience=experience,  
            difficulty=difficulty,
            personality=personality,
            resume_path=resume_path
        )
        if not first_question:
            return await self._finalize_interview()
            #return {"phase": self.phase.value}
    
        self.current_question = first_question
    
        self._set_phase(Phase.AI_SPEAKING)
    
        return {
            "phase": self.phase.value,
            "question": first_question
        }   
    

    async def _process_user_answer(self, answer):
        self._set_phase(Phase.PROCESSING)

        next_question = await self.ai_engine.process_answer(answer)

        if not next_question:
            final_response = await self._finalize_interview()
            return final_response

        self.current_question = next_question

        self._set_phase(Phase.AI_SPEAKING)
        return {
            "phase": self.phase.value,
            "question": next_question
        }

    async def _handle_interrupt(self):  
        self._set_phase(Phase.USER_SPEAKING)

    async def _finalize_interview(self):
        self._set_phase(Phase.FINALIZING)
    
        summary = await self.ai_engine.finalize()
    
        response = None
        if summary:
            response = {
                "phase": self.phase.value,
                "summary": summary
            }
    
        self._set_phase(Phase.IDLE)
        return response

    def _set_phase(self, new_phase: Phase):
        self.phase = new_phase
        print(f"[Controller] Phase changed to: {self.phase}")



async def test_interview_controller():

    ai_engine = AIEngine(mode="TECH")

    controller = InterviewController(ai_engine)

    # Start interview
    response = await controller.handle_event(
        Event.START_INTERVIEW,
        {
            "role": "Data Science",
            "experience": "Fresher",
            "difficulty": "easy",
            "personality": "friendly",
            "resume_path": "practice\Tech\Thasin_Resume.pdf"
        }
    )
    
    print("Interviewer:", response["question"]) 
    #print("Audio:", response["audio"])

    while True:

        answer = input("You: ")
            
        response = await controller.handle_event(
            Event.USER_FINISHED_SPEAKING,
            {"answer": answer}
        )
        if not  response:
            break

        if "summary" in response:
            print("\nInterview Summary:")
            print(response["summary"])
            break

        print("Interviewer:", response["question"])
        
        
        
if __name__ == "__main__":
     asyncio.run(test_interview_controller())
