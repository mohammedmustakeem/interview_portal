import random
from datetime import datetime
from dotenv import load_dotenv
from typing import List,Optional
from practice.Config import config
from pydantic import BaseModel, Field
from practice.Tech.engines.resume_engine import ResumeIntelligence
load_dotenv()

class InterviewEngineState(BaseModel):

    session_id: str
    user_id: str
    role: str
    experience: str
    difficulty: str

    primary_topics: List[str] = Field(default_factory=list)
    secondary_topics: List[str] = Field(default_factory=list)

    current_topic: Optional[str] = None
    last_question: Optional[str] = None
    last_answer: Optional[str] = None
    last_question_type: Optional[str] = None
    last_reaction: Optional[str] = None
    confidence_score: float = 0.5
    performance_score: float = 0

    weak_topics: List[str] = Field(default_factory=list)
    strong_topics: List[str] = Field(default_factory=list)
    covered_topics: List[str] = Field(default_factory=list)
    topic_depth: int = 0
    followup_count: int = 0
    topic_question_count: int = 0
    total_questions: int = 0
    interruption_count: int = 0
    disengagement_count: int = 0
    personality_mode: str = "friendly"
    interview_phase: str = "GREETING"
    end_requested: bool = False
    discussed_projects: str = Field(default_factory=list)
    resume: Optional[ResumeIntelligence] = None
    
    history: Optional[dict] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
