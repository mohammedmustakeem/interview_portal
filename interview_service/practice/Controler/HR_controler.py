from practice.HR.hr import (
    start_interview,
    interview_step,
    record_candidate_answer,
    finalize_hr_interview,
    Message
)

from practice.Tech.engines.resume_engine import *
from practice.Tech.engines.pdf_reader import *



class HREngine:

    def __init__(self, role: str, experience: str, resume_path: str | None = None):

        self.role = role
        self.experience = experience
        self.resume_path = resume_path

        self.state = None

        self.questions = []
        self.answers = []
        self.question_count = 0


       
        # Start Interview
    
    async def start(self, resume_path:str = None):

        self.state = start_interview(
            role=self.role,
            experience=self.experience
        )
        if resume_path:

            print("Parsing resume...")
        
            text = PDFTextExtractor.extract_text(resume_path)
        
            parser = ResumeParser()
            resume_data = parser.parse(text, self.role)
        
            resume_intel = to_resume_intelligence(resume_data)
        
            self.state.resume = resume_intel
        
            print("Resume parsed successfully.")
            print("Projects found:", [p.name for p in resume_intel.projects])
    
        return await self._next_question()



    # Generate next question
   
    async def _next_question(self):

        if not self.state.active:
            return None

        self.state = interview_step(self.state)

        question = self.state.messages[-1].content

        self.question_count += 1
        self.questions.append(question)

        return question


     
        # Process Candidate Answer
    async def process_answer(self, answer: str):

        if answer.lower() in ["exit", "quit", "done"]:

            return finalize_hr_interview(
        self.answers,
        self.questions,
        self.question_count
        )

        self.answers.append(answer)
    
        self.state = record_candidate_answer(self.state, answer)
    
        if not self.state.active:
            return None

        return await self._next_question()


   
    # Finalize Interview
    async def finalize(self):
    
        return finalize_hr_interview(
        self.answers,
        self.questions,
        self.question_count
    )
