from practice.Controler.HR_controler import HREngine
from practice.Controler.tech_controler import TechEngine
import asyncio



class AIEngine:

    def __init__(self, mode, config=None):
        self.mode = mode
        self.engine = None
        self.config = config

    async def start(self, role, experience, difficulty=None, personality=None, resume_path = None):
        if self.mode == "HR":
            self.engine = HREngine(
                role=role,
                experience=experience
            )
            return await self.engine.start(resume_path=resume_path)

        elif self.mode == "TECH":
            self.engine = TechEngine(
                role=role,
                experience=experience,
                difficulty=difficulty,
                personality=personality
            )
            
            return await self.engine.start(resume_path=resume_path)

    async def process_answer(self, answer):
        return await self.engine.process_answer(answer)

    async def finalize(self):
        return await self.engine.finalize()


# import asyncio

# async def test_ai_engine():

#     ai_engine = AIEngine(mode="TECH")

#     question = await ai_engine.start(
#         role="Data Scientist",
#         experience="1 year",
#         difficulty="easy",
#         personality="strict",
#         resume_path="practice\Tech\engines\Thasin_Resume.pdf"
#     )

#     print("TECH Interview Started")
#     print("Interviewer:", question)

#     while True:
#         answer = input("You: ")

#         response = await ai_engine.process_answer(answer)
#         print("Interviewer:", response)

#         if "Interview finished" in response:
#             break


# if __name__ == "__main__":
#     asyncio.run(test_ai_engine())
