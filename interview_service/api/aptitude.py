from practice.utils import list_topic, get_aptitude_question, load_topics
from fastapi import APIRouter,HTTPException
import random
router = APIRouter(prefix='/aptitude', tags=['Aptitude_round'])


@router.post('/topic')
def get_topics():
    return {'topic': list_topic}


@router.get("/questions/{topic}")
def get_questions(topic: str, difficulty: str, count: int = 10):

    difficulty = difficulty.strip().lower()

    data = load_topics(topic)

    if not isinstance(data, list) or len(data) == 0:
        raise HTTPException(status_code=404, detail="No questions found")

    # STRICT filter
    filtered = []

    for q in data:
        q_diff = str(q.get("difficulty", "")).strip().lower()
        if q_diff == difficulty:
            filtered.append(q)

    if len(filtered) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No {difficulty} questions found for {topic}"
        )

    count = min(count, len(filtered))

    selected = random.sample(filtered, count)

    sanitized = [
        {
            "question": q["question"],
            "options": q["options"],
            "difficulty": q.get("difficulty"),
            "concept_id": q.get("concept_id"),
            "correct_option": q.get("correct_option"),
        }
        for q in selected
    ]

    return {
        "topic": topic,
        "difficulty": difficulty,
        "count": count,
        "questions": sanitized
    }
