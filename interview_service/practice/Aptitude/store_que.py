import os
import json
from practice.Aptitude.role_based_generator import generate_role_session
from practice.Aptitude.session_generator import generate_question_batch
import os
import json
import uuid


BASE_PATH = "practice/data/question_bank"
TOPIC_GROUP_MAP = {
    # Math
    "STAT_MEAN": "statistics",
    "STAT_WEIGHTED_MEAN": "statistics",
    "STAT_MEDIAN": "statistics",
    "STAT_MODE": "statistics",
    "STAT_VARIANCE": "statistics",
    "STAT_STD_DEV": "statistics",
    "STAT_PROBABILITY_BASIC": "statistics",

    # Logical
    "logical_reasoning": "logical_reasoning",

    # Role / non-math
    "decision_making": "decision_making",
    "analytical_thinking": "analytical_thinking",
    "situational_judgement": "situational_judgement",
    "business_judgement": "business_judgement",
}
def resolve_category(q):
    if "concept_id" in q:   # math question
        return TOPIC_GROUP_MAP.get(q["concept_id"], "statistics")

    # role / non-math
    return TOPIC_GROUP_MAP.get(q["category"], q["category"])

def get_file_name(q):
    # Math aptitude → concept_id
    return f"{q['category']}.json"


def get_file_path(q):
    return os.path.join(BASE_PATH, get_file_name(q))

def load_existing_questions(category):
    path = get_file_path(category)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def question_signature(q):
    return q["question"].strip().lower()


def validate_unified_question(q):
    return (
        isinstance(q, dict)
        and isinstance(q.get("question"), str)
        and isinstance(q.get("options"), dict)
        and q.get("correct_option") in q.get("options", {})
        and isinstance(q.get("category"), str)
        and isinstance(q.get("difficulty"), str)
    )

def load_existing(FILE_PATH):
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def store_questions_unified(questions):
    os.makedirs(BASE_PATH, exist_ok=True)

    for q in questions:
        if not validate_unified_question(q):
            print("❌ Invalid skipped")
            continue

        category = q["category"]
        path = os.path.join(BASE_PATH, f"{category}.json")

        existing = load_existing(path)
        signatures = {question_signature(x) for x in existing}

        sig = question_signature(q)
        if sig in signatures:
            print("⚠️ Duplicate skipped")
            continue

        q["id"] = str(uuid.uuid4())
        existing.append(q)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved to {category}.json")
unified_math = []

math_questions = generate_question_batch(user_id="8", aptitude_type="Arithmetic", topic="Profit & Loss", difficulty="easy", total_questions=5)


def clean_question(text):
    return text.replace("**Rewritten Question:**", "").strip()
def normalize_options(options_list):
    labels = ["A", "B", "C", "D"]
    return {label: opt for label, opt in zip(labels, options_list)}

for q in math_questions:
    unified_math.append({
        "question": clean_question(q["question"]),
        "options": normalize_options(q["options"]),
        "correct_option": [
            k for k, v in normalize_options(q["options"]).items()
            if v == q["correct_answer"]
        ][0],
        "explanation": f"Computed using formula: {q['meta']['formula']}",
        "category": resolve_category(q),
        "difficulty": q["difficulty"],
        "subtopic": q["concept_id"]
    })


cate = "business_judgement"
diffi = "easy"
role_questions = generate_role_session(
    category=cate,
    difficulty=diffi,
    total_questions=2
)
print(role_questions)
unified_role = []

for q in role_questions:
  unified_role.append({
        "question": q["question"].strip(),
        "options": q["options"],  # already dict
        "correct_option": q["correct_option"],
        "explanation": q.get("explanation", ""),
        "category": cate,
        "difficulty": diffi,
        "subtopic": q.get("subtopic")
    })

store_questions_unified(unified_role)
store_questions_unified(unified_math)
