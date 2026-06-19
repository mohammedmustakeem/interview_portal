from pydantic import BaseModel, Field
from typing import Literal

class GenerateRequest(BaseModel):
    engine: Literal["session", "role"]        # which engine to use
    topic: str = Field(..., example="profit and loss")
    difficulty: Literal["easy", "medium", "hard"]
    count: int = Field(..., ge=1, le=50)
    user_id: str = Field(default="admin")

class GenerateResponse(BaseModel):
    status: str
    engine: str
    requested: int
    saved: int
    skipped_duplicates: int
    skipped_invalid: int
    
import os
import json
import uuid
import logging
from practice.Aptitude.session_generator import generate_question_batch

logger = logging.getLogger(__name__)
BASE_PATH = "practice/data/question_bank"
STATUS_EXHAUSTED = "EXHAUSTED"


def question_signature(q: dict) -> str:
    concept_id = q.get("concept_id", "")
    params = q.get("params", {})
    sorted_params = "_".join(f"{k}={v}" for k, v in sorted(params.items()))
    return f"{concept_id}__{sorted_params}"


def load_existing(file_path: str) -> list:
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def convert_and_validate(q: dict) -> dict | None:
    if q.get("status") == STATUS_EXHAUSTED:
        return None

    labels = ["A", "B", "C", "D"]
    options_dict = {labels[i]: opt for i, opt in enumerate(q["options"])}
    correct_option = next(
        (k for k, v in options_dict.items() if v == q["correct_answer"]), None
    )
    if not correct_option:
        return None

    unified = {
        "question": q["question"].replace("**Rewritten Question:**", "").strip(),
        "options": options_dict,
        "correct_option": correct_option,
        "explanation": f"Computed using {q['meta']['formula']}",
        "category": q["topic"],
        "difficulty": q["difficulty"],
        "concept_id": q["concept_id"],
        "params": q.get("params", {}),
        "source": "session",            # ← tag which engine produced it
    }

    if unified["correct_option"] not in unified["options"]:
        return None

    return unified


def store_questions(questions: list) -> dict:
    os.makedirs(BASE_PATH, exist_ok=True)
    saved, skipped_dup, skipped_invalid = 0, 0, 0

    for q in questions:
        unified = convert_and_validate(q)
        if not unified:
            skipped_invalid += 1
            continue

        category = unified["category"].replace(" ", "_")
        path = os.path.join(BASE_PATH, f"{category}.json")
        existing = load_existing(path)
        signatures = {question_signature(x) for x in existing}

        if question_signature(unified) in signatures:
            skipped_dup += 1
            continue

        unified["id"] = str(uuid.uuid4())
        existing.append(unified)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
            saved += 1

            return {"saved": saved, "skipped_duplicates": skipped_dup, "skipped_invalid": skipped_invalid}


async def run(topic: str, difficulty: str, count: int, user_id: str) -> dict:
    questions = generate_question_batch(
        user_id=user_id,
        aptitude_type="Arithmetic",
        topic=topic,
        difficulty=difficulty,
        total_questions=count,
    )
    return store_questions(questions)
