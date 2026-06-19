import random
from practice.Aptitude.generator import build_question
from practice.Aptitude.concepts.topic_concepts import ALL_CONCEPTS
from collections import defaultdict
from practice.utils import normalize
from practice.utils import FINAL_QUESTION_HASHES


NORMALIZED_ALL_CONCEPTS = {}

for aptitude, topics in ALL_CONCEPTS.items():
    n_apt = normalize(aptitude)
    #print("n_apt is ", n_apt)
    NORMALIZED_ALL_CONCEPTS[n_apt] = {}

    for topic, concept_ids in topics.items():
        n_topic = normalize(topic)
        NORMALIZED_ALL_CONCEPTS[n_apt][n_topic] = concept_ids


def generate_question_batch(
    user_id: str,
    aptitude_type: str,
    topic: str,
    difficulty: str,
    total_questions: int = 20
):
    FINAL_QUESTION_HASHES.clear()
    aptitude_type = normalize(aptitude_type)
    topic = normalize(topic)
    topic = topic.replace("_", " ")
    seen_question_ids = set()
    questions = []

    # ------------------ DI CASELET ------------------
    eligible_concepts = NORMALIZED_ALL_CONCEPTS.get(
    aptitude_type,{}).get(topic, [])

    if not eligible_concepts:
        available = sorted(
            set(cfg.get("sub_topic") for cfg in ALL_CONCEPTS.values())
        )
        raise ValueError(
            f"No concepts found for aptitude_type={aptitude_type}, topic={topic}\n"
            f"Available sub_topics={available}"
        )

    MAX_ATTEMPTS = total_questions * 5
    attempts = 0

    concept_usage = defaultdict(int)
    available_concepts = eligible_concepts.copy()

    MAX_PER_CONCEPT = max(1, total_questions // len(eligible_concepts))

    while len(questions) < total_questions and attempts < MAX_ATTEMPTS:
        attempts += 1

        if not available_concepts:
            break

        concept_id = random.choice(available_concepts)
   
        q = build_question(
            concept_id=concept_id,
            difficulty=difficulty,
            user_id=user_id,
            user_role="NA",
            user_type=aptitude_type,
            user_topic=topic
        )
        q['topic'] = topic
        if q.get("status") == "EXHAUSTED":
            available_concepts.remove(concept_id)
            continue

        if q["question_id"] in seen_question_ids:
            continue

        seen_question_ids.add(q["question_id"])
        questions.append(q)
        concept_usage[concept_id] += 1

        if concept_usage[concept_id] >= MAX_PER_CONCEPT:
            available_concepts.remove(concept_id)
        
    return questions

questions = generate_question_batch(user_id="35", aptitude_type="Arithmetic", topic="percentages", difficulty="hard", total_questions=6)

# print(questions)

BASE_PATH = "practice/data/question_bank"
import os
import json
import uuid

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

def load_existing(FILE_PATH):
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def question_signature(q):
    return q["question"].strip().lower()

def normalize_options(options_list):
    labels = ["A", "B", "C", "D"]
    return {labels[i]: opt for i, opt in enumerate(options_list)}
def extract_correct_option(options_dict, correct_answer):
    for k, v in options_dict.items():
        if v == correct_answer:
            return k
    return None
def convert_math_to_unified(q):
    options_dict = normalize_options(q["options"])
    correct_option = extract_correct_option(
        options_dict, q["correct_answer"]
    )

    if not correct_option:
        return None

    return {
        "question": q["question"].replace("**Rewritten Question:**", "").strip(),
        "options": options_dict,
        "correct_option": correct_option,
        "explanation": f"Computed using {q['meta']['formula']}",
        "category": q["topic"],              # statistics
        "difficulty": q["difficulty"],
        "concept_id": q["concept_id"]         # for tracking
    }

def validate_unified_question(q):
    return (
        isinstance(q, dict)
        and isinstance(q.get("question"), str)
        and isinstance(q.get("options"), dict)
        and q.get("correct_option") in q.get("options", {})
        and isinstance(q.get("topic"), str)
        and isinstance(q.get("difficulty"), str)
    )
def store_questions(questions):
    os.makedirs(BASE_PATH, exist_ok=True)

    for q in questions:
        unified = convert_math_to_unified(q)
        if not unified:
            print(" Invalid skipped")
            continue

        category = unified["category"]
        category = category.replace(" ", "_")
        path = os.path.join(BASE_PATH, f"{category}.json")

        existing = load_existing(path)
        signatures = {question_signature(x) for x in existing}

        sig = question_signature(unified)
        if sig in signatures:
            print(" Duplicate skipped")
            continue

        unified["id"] = str(uuid.uuid4())
        existing.append(unified)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        print(f" Saved to {category}.json")


# store_questions(questions)
