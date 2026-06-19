import random
import os
from openai import AsyncOpenAI
from practice.Tech.engines.topic_engine import TopicEngine
from practice.Tech.engines.decision_engine import DecisionEngine
from practice.Tech.engines.personality_engine import PersonalityEngine
from practice.Tech.Question_generator import QuestionGenerator
from practice.Tech.engines.answer_analyzer import AnswerAnalyzer
from practice.Tech.engines.interview_engine import InterviewEngineState
from practice.Tech.engines.pdf_reader import PDFTextExtractor
from practice.Tech.engines.resume_engine import ResumeParser, to_resume_intelligence
from practice.Tech.engines.final_evaluation_engine import FinalReportEngine

class TechEngine:

    def __init__(self, role: str, experience: str, difficulty: str, personality):

        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
            )

        self.topic_engine = TopicEngine(self.client)
        self.decision_engine = DecisionEngine()
        self.personality_engine = PersonalityEngine()
        self.question_engine = QuestionGenerator(self.client)
        self.answer_analyzer = AnswerAnalyzer(self.client)
        self.final_report_engine = FinalReportEngine(self.client)
        self.role = role
        self.experience = experience
        self.difficulty = difficulty
        self.personality = personality or "friendly"

        self.state = None

    # Start Interview
    async def start(self, resume_path=None):
        print("Before generate_topics")

        topics = await self.topic_engine.generate_topics(
            role=self.role,
            experience=self.experience,
            difficulty=self.difficulty
        )
        print("After generate_topics")
        random.shuffle(topics.primary_topics)

        self.state = InterviewEngineState(
            session_id="live_session",
            user_id="user",
            role=self.role,
            experience=self.experience,
            difficulty=self.difficulty,
            primary_topics=topics.primary_topics,
            secondary_topics=topics.secondary_topics,
            current_topic=random.choice(topics.primary_topics),
            personality_mode=self.personality,
            interview_phase="GREETING"
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
        greeting = f"""
       Welcome. Today's mock interview for the {self.role} role will explore your projects, your experience as a {self.experience}, and core technical concepts.

       Let's begin.
        """.strip()
        self.state.interview_phase = 'TECHNICAL'
        
        return greeting + await self._generate_next_question()
    
        # Process User Answer
    async def process_answer(self, answer: str):

        if answer.lower() in ["exit", "quit", "done"]:
            return None

        #  Analyze answer
        self.state = await self.answer_analyzer.analyze(self.state, answer)
        
        #  Check disengagement
        if self.state.disengagement_count >= 3:
            return "It seems this may not be the right time. Let's pause here."

        #  Rotate topic if needed
        if self.state.topic_question_count >= 3:
            self.state.covered_topics.append(self.state.current_topic)
            self.state.current_topic = self.decision_engine.select_next_topic(self.state)
            self.state.topic_question_count = 0
            self.state.topic_depth = 0

        return await self._generate_next_question()
    # Generate Question
    
    async def _generate_next_question(self):

        decision = self.decision_engine.decide(self.state)

        personality_prompt = self.personality_engine.build_prompt(
            self.state.personality_mode
        )

        generated = await self.question_engine.generate(
            self.state,
            decision,
            personality_prompt
        )
        
        self.state.topic_depth += 1
        self.state.last_reaction = generated.reaction
        speech = f"{generated.reaction}\n\n{generated.question}"
        
        if self.state.interview_phase == "GREETING":
            self.state.interview_phase = "TECHNICAL"
        # Update state
        self.state.last_question = generated.question
        self.state.last_question_type = decision["question_type"]
        self.state.topic_question_count += 1
        self.state.total_questions += 1
        return speech

    # Finalize Interview
    async def finalize(self):

        report = await self.final_report_engine.generate(self.state)
        return f"""
        Interview Finished
        Overall Score: {report['overall_score']}
        Candidate Level: {report['candidate_level']}
        Strengths:
            {chr(10).join("- "+s for s in report['strengths'])}
        Weaknesses:
            {chr(10).join("- "+s for s in report['weaknesses'])}
        Topics to Improve:
            {chr(10).join("- "+s for s in report['topics_to_improve'])}
        Final Feedback:
            {report['final_feedback']}
        """