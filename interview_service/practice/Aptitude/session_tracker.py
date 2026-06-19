from pydantic import BaseModel, Field, validator
from typing import Dict, Literal
from practice.Config import config

class SessionTracker:
    def __init__(self):
        self.asked_concepts = set()
        self.topic_count = {}
        self.correct_streak = 0

    def can_ask(self, concept_id, topic):
        if concept_id in self.asked_concepts:
            return False
        if self.topic_count.get(topic, 0) >= 3:
            return False
        return True

    def register(self, concept_id, topic, correct=False):
        self.asked_concepts.add(concept_id)
        self.topic_count[topic] = self.topic_count.get(topic, 0) + 1

        if correct:
            self.correct_streak += 1
        else:
            self.correct_streak = 0

class RoleSessionState:
    def __init__(self):
        self.asked_signatures = set()
        self.dimension_count = {}
        self.responses = []

    def signature(self, mcq):
        return (
            mcq["dimension"],
            mcq["correct_option"],
            tuple(mcq["options"].values())
        )

    def is_duplicate(self, mcq):
        sig = self.signature(mcq)
        if sig in self.asked_signatures:
            return True
        self.asked_signatures.add(sig)
        return False

    def register_dimension(self, dimension):
        self.dimension_count[dimension] = self.dimension_count.get(dimension, 0) + 1

class RoleMCQ(BaseModel):
    question: str = Field(..., min_length=10)

    options: Dict[Literal["A", "B", "C", "D"], str]

    correct_option: Literal["A", "B", "C", "D"]

    dimension: str

    explanation: str = Field(..., min_length=10)

    # ---------- Validators ----------

    @validator("dimension")
    def dimension_must_be_allowed(cls, v):
        if v not in config.ALLOWED_DIMENSIONS:
            raise ValueError(f"Invalid dimension: {v}")
        return v

    @validator("options")
    def options_must_be_unique(cls, v):
        if len(set(v.values())) != 4:
            raise ValueError("Options must be unique")
        return v

    @validator("correct_option")
    def correct_option_must_exist(cls, v, values):
        options = values.get("options", {})
        if v not in options:
            raise ValueError("Correct option not in options")
        return v

    @validator("question")
    def avoid_definition_questions(cls, v):
        forbidden = ["what is", "define", "means", "refers to"]
        if any(word in v.lower() for word in forbidden):
            raise ValueError("Definition-style question not allowed")
        return v
