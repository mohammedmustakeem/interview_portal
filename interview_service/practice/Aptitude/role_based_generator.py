import random
import re
import json
import os
from collections import Counter
from dotenv import load_dotenv
from practice.Aptitude.wording_llm import generate_role_mcq_batch
from practice.Aptitude.session_tracker import RoleSessionState
from practice.Aptitude.formula_engine.topic_map import TOPIC_MAP
from practice.utils import parse_mcq_text, plan_subtopics, split_mcq_blocks,auto_verify_role_question


def generate_role_session(category, difficulty, total_questions):
    subtopics = TOPIC_MAP[category]

    subtopic_plan = plan_subtopics(
        subtopics=subtopics,
        total=total_questions,
        max_per_subtopic=3
    )

    questions = []
    seen_questions = set()

    BATCH_SIZE = 5
    idx = 0

    while len(questions) < total_questions:
        batch_subtopics = subtopic_plan[idx: idx + BATCH_SIZE]
        idx += BATCH_SIZE

        if not batch_subtopics:
            break

        raw_text = generate_role_mcq_batch(
            category=category,
            difficulty=difficulty,
            subtopics=batch_subtopics,  
        )

        blocks = split_mcq_blocks(raw_text)
        # print("raw_text " ,raw_text)
        # print("blocks ", blocks)
        
        for block in blocks:
            mcq = parse_mcq_text(block)
            if not mcq:
                continue
            signature = mcq["question"].strip().lower()
            if signature in seen_questions:
                continue

            mcq["category"] = category
            mcq['difficulty'] = difficulty
            if not auto_verify_role_question(mcq):
                continue

            seen_questions.add(signature)
            questions.append(mcq)

            if len(questions) >= total_questions:
                break
           
            
    return questions


def evaluate_role_session(questions, user_answers):
    score = 0
    category_score = {}

    for q, user_ans in zip(questions, user_answers):
        if user_ans == q["correct_option"]:
            score += 1
            cat = q["category"]
            category_score[cat] = category_score.get(cat, 0) + 1

    return {
        "score": score,
        "out_of": len(questions),
        "category_score": category_score
    }
    
    

BASE_PATH = "practice/data/question_bank"

def get_file_path(category):
    return os.path.join(BASE_PATH, f"{category}.json")


def load_existing_questions(category):
    path = get_file_path(category)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def question_signature(q):
    return q["question"].strip().lower()


def validate_question(q):
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


def store_questions(questions):
    os.makedirs(BASE_PATH, exist_ok=True)

    for q in questions:
        if not validate_question(q):
            print(" Invalid question skipped")
            continue

        category = q["category"]
        path = get_file_path(category)

        existing = load_existing_questions(category)
        signatures = {question_signature(x) for x in existing}

        sig = question_signature(q)
        if sig in signatures:
            print(" Duplicate skipped")
            continue

        existing.append(q)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        print(f" Saved to {category}.json")
        

cate = "business_judgement"
diffi = "medium"
role_questions = generate_role_session(
    category=cate,
    difficulty=diffi,
    total_questions=5
)
# store_questions(role_questions)


# print(role_questions)

