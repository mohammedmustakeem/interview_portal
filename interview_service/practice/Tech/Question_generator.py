from pydantic import BaseModel
from typing import List
from openai import AsyncOpenAI
import json
import re
from dotenv import load_dotenv
from practice.Tech.engines.topic_engine import TopicEngine
import random

load_dotenv()

class GeneratedQuestion(BaseModel):
    reaction:str = ""
    question: str
    expected_depth: str  # basic | intermediate | deep
    evaluation_points: List[str]
    probing_angles: List[str]


class QuestionGenerator:

    def __init__(self, client: AsyncOpenAI):
        self.client = client

    # ---- Clean JSON from markdown wrapper ----
    def _extract_json(self, text: str) -> dict:
        """
        Extract JSON safely even if wrapped in ```json blocks
        """
        match = re.search(r"```json(.*?)```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()

        return json.loads(text)

    # ---- Prompt Builder ----
    def _build_prompt(self, state, decision, personality_instruction: str, selected_item, resume_focus) -> str:
         
        
        resume_section = ""
        if resume_focus == "project" and selected_item:
            resume_section = f"""
            Focus on this Resume Project:
            Example:
            Start question with You mention,I also noticed in your resume {selected_item}, In your resume, I see in your resume you mention etc..

            Project Name: {selected_item.name}
            Technologies: {selected_item.technologies}
            
            Ask about:
            - Architecture
            - Why chosen
            - Challenges
            - Scaling
            """
        elif resume_focus == "skill" and selected_item:
            resume_section = f"""
        Focus on this Resume Skill:
        example:
        Start question with You mention,I also noticed in your resume {selected_item} In your resume, I see in your resume you mention etc..
        Skill: {selected_item}
        
        Ask:
        - Depth of understanding
        - Real-world usage
        - Edge cases
        - Trade-offs
        """ 
        
        prompt = f"""
                 You are a senior engineer conducting a real technical interview.
                 
                 ROLE: {state.role}
                 EXPERIENCE: {state.experience}
                 TOPIC: {state.current_topic}
                 TYPE: {decision['question_type']}
                 LEVEL: {decision['difficulty']}
                 
                 {resume_section}
                 
                 Context:
                     Last Question: {state.last_question}
                     Candidate Answer: {state.last_answer}
                     Last Reaction: {state.last_reaction}
                 
                     {personality_instruction}
                 
                     Rules:
                 
                         1. Always respond in this order:
                             - short reaction to candidate answer
                             - one follow-up question
                 
                             2. Behavior:
                                 - good answer → acknowledge + deeper question
                                 - weak answer → guide + simpler question
                                 - refusal → calm redirect
                                 - meta question → short reply then continue
                 
                                 3. Conversation style:
                                     - natural interviewer tone
                                     - concise
                                     - avoid repeating questions
                                     - ask only ONE question
                                         Return ONLY JSON:
                 
                                             {{
                                                 "react ion": "short interviewer response",
                                                 "question": "next interview question",
                                                 "expected_depth": "basic | intermediate | deep",
                                                 "evaluation_points": ["concept1","concept2"],
                                                 "probing_angles": ["angle1","angle2"]
                                             }}
                                             """
        return prompt
    # ---- Main Generate Function ----
    async def generate(self, state, decision, personality_instruction: str) -> GeneratedQuestion:
       
        selected_item = None
        resume_focus = None
        
        if decision["question_type"] == "resume_based" and state.resume:
            # Priority order: project → skill → certification
            if state.resume.projects:
                available = [
                    p for p in state.resume.projects
                    if p.name not in state.discussed_projects
                ]
        
                if not available:
                    available = state.resume.projects
        
                    selected_item = random.choice(available)
                    resume_focus = "project"
                    # mark discussed
                    state.discussed_projects.append(selected_item.name)
        
                elif state.resume.skills:
                    selected_item = random.choice(state.resume.skills)
                    resume_focus = "skill"
        
                elif state.resume.certifications:
                    selected_item = random.choice(state.resume.certifications)
                    resume_focus = "certification"
                        
        prompt = self._build_prompt(state, decision, personality_instruction, selected_item, resume_focus)
        print("Before QuestionGenerator API Call")
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior technical interviewer. Always return valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )
        print("After QuestionGenerator API Call")

        raw_content = response.choices[0].message.content.strip()

        try:
            parsed = self._extract_json(raw_content)
            print("QuestionGenerator parsing successful")
            return GeneratedQuestion(**parsed)
        
        
        except Exception as e:
        
            print("QuestionGenerator parsing failed:", e)
            print("Raw LLM Output:", raw_content)
        
            return GeneratedQuestion(
                question="Can you explain your approach in more detail?",
                expected_depth="intermediate",
                evaluation_points=["clarity", "technical reasoning"],
                probing_angles=["implementation details", "edge cases"]
            )
        
# from practice.Tech.engines.interview_engine import InterviewEngineState 
# async def test():
#     client = AsyncOpenAI()
#     engine = TopicEngine(client)

#     topics = await engine.generate_topics(
#         role="data science",
#         difficulty="easy",
#         experience="1 year"
#     )
#     print(topics)
#     state = InterviewEngineState(
#         session_id="test123",
#         user_id="user1",
#         role="Data Science",
#         experience="1 year",
#         difficulty="easy",
#         primary_topics=topics.primary_topics,
#         secondary_topics=topics.secondary_topics,
#         current_topic=topics.primary_topics[0] if topics.primary_topics else None,
#         personality_mode="strict"
#     )
#     personality_instruction =  "Tone: Professional and strict. Ask directly."
#     question = QuestionGenerator(client)
#     result = await question.generate(state, {'question_type':"scenario", "difficulty": "easy"}, personality_instruction)
#     print(result)
    
# import asyncio
# if __name__ == "__main__":
#     asyncio.run(test())







