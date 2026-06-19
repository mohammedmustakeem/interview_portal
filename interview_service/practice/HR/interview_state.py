import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from practice.Tech.engines.resume_engine import ResumeIntelligence


class Message(BaseModel):
    role: Literal["hr", "candidate"]
    content: str


class HRInterviewState(BaseModel):
    # Identity
    session_id: str
    user_id: Optional[str] = None

    # Job context
    role: str
    experience: str

    # Interview flow
    stage: str = "intro"                      # current STAGE_ORDER value
    context_focus: str = "intro"              # topic the LLM is focusing on
    context_question_count: int = 0           # questions asked in current focus
    total_questions: int = 0
    active: bool = True

    # Short-term memory (avoids re-reading full history each turn)
    last_question: Optional[str] = None
    last_answer: Optional[str] = None
    last_reaction: Optional[str] = None
    last_question_type: Optional[str] = None
    # Candidate behaviour counters
    interruption_count: int = 0
    disengagement_count: int = 0
    end_requested: bool = False
    personality_mode: str = "friendly"
    interview_phase: str = "GREETING"
    # Scores
    communication_score: float = 5.0
    performance_score: float = 0.5
    confidence_score: float = 0.5
    hr_score: float = 5.0
    resume_questions_asked: int = 0
    # Qualitative observations
    strong_topics: List[str] = Field(default_factory=list)
    weak_topics: List[str] = Field(default_factory=list)
    discussed_projects: List[str] = Field(default_factory=list)
    resume: Optional[ResumeIntelligence] = None
    # Full conversation history
    messages: List[Message] = Field(default_factory=list)

    # Timestamps — use datetime.datetime (not bare datetime)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    model_config = {"arbitrary_types_allowed": True}          # Pydantic v2

    # Allow direct attribute mutation (critical — Pydantic v2 is immutable by default)
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
