import os
import json
import uuid
import logging
from practice.Aptitude.role_based_generator import generate_role_session
from practice.Aptitude.formula_engine.topic_map import TOPIC_MAP

logger = logging.getLogger(__name__)
BASE_PATH = "practice/data/question_bank"


def question_signature(q: dict) -> str:
    # role questions don't have params, so text-based sig is fine here
    return q["question"].strip().lower()


def load_existing(file_path: str) -> list:
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(q: dict) -> bool:
    return (
isinstance(q, dict)
and "question" in q
and "options" in q
and "correct_option" in q
and "category" in q
and len(q["options"]) == 4
and q["correct_option"] in q["options"]
and q["question"].strip().endswith("?")
)


def store_questions(questions: list) -> dict:
    os.makedirs(BASE_PATH, exist_ok=True)
    saved, skipped_dup, skipped_invalid = 0, 0, 0

    for q in questions:
        if not validate(q):
            skipped_invalid += 1
            continue

        category = q["category"].replace(" ", "_")
        path = os.path.join(BASE_PATH, f"{category}.json")
        existing = load_existing(path)
        signatures = {question_signature(x) for x in existing}

        if question_signature(q) in signatures:
            skipped_dup += 1
            continue

        q["id"] = str(uuid.uuid4())
        q["source"] = "role"             # ← tag which engine produced it
        existing.append(q)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
            saved += 1

            return {"saved": saved, "skipped_duplicates": skipped_dup, "skipped_invalid": skipped_invalid}


async def run(topic: str, difficulty: str, count: int, user_id: str) -> dict:
    if topic not in TOPIC_MAP:
        raise ValueError(f"Topic '{topic}' not found in TOPIC_MAP. Available: {list(TOPIC_MAP.keys())}")

    questions = generate_role_session(
        category=topic,
        difficulty=difficulty,
        total_questions=count,
    )
    return store_questions(questions)
