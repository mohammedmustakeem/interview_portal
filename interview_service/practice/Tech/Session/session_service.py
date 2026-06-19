from practice.Tech.Session.session_repo import SessionRepository
from practice.Tech.engines.interview_engine import InterviewEngineState
from practice.Tech.engines.topic_engine import TopicEngine
from uuid import uuid4


class SessionService:

    def __init__(self, repository: SessionRepository, topic_engine:TopicEngine):
        self.repo = repository
        self.topic_engine = topic_engine

    async def start_session(self,user_id: str,role: str,experience: str,difficulty: str,personality: str = "friendly") -> InterviewEngineState:
        
        topics = await self.topic_engine.generate_topics(role, difficulty, experience)
        
        first_topic = topics.primary_topics[0] if topics.primary_topics else None
        
        session = InterviewEngineState(
         session_id=str(uuid4()),
         user_id=user_id,
         role=role,
         experience=experience,
         difficulty=difficulty,
         primary_topics=topics.primary_topics,
         secondary_topics=topics.secondary_topics,
         current_topic=first_topic,
         personality_mode=personality
         )
        
        await self.repo.create(session.model_dump())

        return session

    async def get_session(self, session_id: str) -> InterviewEngineState | None:
        if not session_id or not session_id.strip():
            raise ValueError("Session id cannot be empty")
        
        data = await self.repo.get(session_id)

        if not data:
            return None

        try:
            return InterviewEngineState(**data)
        except Exception as e:
            
            print(f"Failed to deserialize session {session_id}: {e}")
            return None            
            
    async def update_scores(self,session_id: str,confidence: float,performance: float):
        await self.repo.update(session_id, {
            "confidence_score": confidence,
            "performance_score": performance
        })

    async def update_topic(self,session_id: str,topic: str,question_type: str):
        await self.repo.update(session_id, {
            "current_topic": topic,
            "last_question_type": question_type
        })

    async def add_question_answer(self,session_id: str,question: str,answer: str):
        
        await self.repo.push_to_array(session_id,"covered_topics",question)
        await self.repo.push_to_array(session_id,"covered_topics",answer)
