import json
import os
import hashlib
import random
import re
#from practice.Config. import LOGICAL_DISTRACTORS
from typing import Counter
from practice.Config import config
from practice.Aptitude.formula_engine.formula_engine import FORMULA_REGISTRY

STORE_PATH = "practice/data/question_store.json"

def param_signature(concept_id, params):
    normalized = []

    for k, v in sorted(params.items()):
        if isinstance(v, list):
            normalized.append(tuple(sorted(v)))
        else:
            normalized.append(v)

    return f"{concept_id}_" + str(hash(tuple(normalized)))


def load_store():
    # File does not exist
    if not os.path.exists(STORE_PATH):
        return {}

    # File exists but empty
    if os.path.getsize(STORE_PATH) == 0:
        return {}

    try:
        with open(STORE_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Corrupted JSON recovery
        return {}

    # Backward compatibility (old list format)
    if isinstance(data, list):
        return {}

    return data

def save_store(data):
    with open(STORE_PATH, "w") as f:
        json.dump(data, f, indent=2)
        
        
def is_new_question(user_id, concept_id, signature):
    store = load_store()

    return (
        user_id not in store
        or concept_id not in store[user_id]
        or signature not in store[user_id][concept_id]
    )

def register_question(user_id, concept_id, signature):
    store = load_store()

    store.setdefault(user_id, {})
    store[user_id].setdefault(concept_id, [])
    store[user_id][concept_id].append(signature)

    with open(STORE_PATH, "w") as f:
        json.dump(store, f, indent=2)



def get_concepts_by_type_and_topic(concept_registry, aptitude_type, topic):
    concepts = concept_registry.get(aptitude_type, {})
    return {
        cid: cfg
        for cid, cfg in concepts.items()
        if cfg["topic"] == topic
    }

def get_concepts_by_type_and_topic(concept_registry, aptitude_type, topic):
    concepts = concept_registry.get(aptitude_type, {})
    return {
        cid: cfg
        for cid, cfg in concepts.items()
        if cfg["topic"] == topic
    }


def reset_user_store(user_id):
    store = load_store()
    if user_id in store:
        del store[user_id]

    with open(STORE_PATH, "w") as f:
        json.dump(store, f, indent=2)


def fill_placeholders(text: str, params: dict, param_aliases: dict) -> str:
    """
    Replace placeholders like {speed}, {v}, {distance}, etc.
    Safe replacement using aliases.
    """
    for canonical, aliases in param_aliases.items():
        if canonical not in params:
            raise ValueError(
                f"[PARAM ERROR] Missing '{canonical}' in params. "
                f"Available params: {list(params.keys())}"
            )

        value = params[canonical]
        for alias in aliases:
            text = text.replace(f"{{{alias}}}", str(value))

    return text


def is_number(x):
    return isinstance(x, (int, float))

def normalize(x):
    if not isinstance(x, str):
        return ""
    x = x.lower()
    x = x.replace("–", "-")   # normalize EN DASH
    x = x.replace("&", "and")
    x = re.sub(r"[^a-z0-9\s-]", "", x)  # remove symbols
    x = re.sub(r"\s+", " ", x).strip()
    return x


def extract_number(text):
    match = re.search(r"-?\d+(\.\d+)?", str(text))
    return float(match.group()) if match else None

def build_ranking_options(correct_value: int):
    """
    Ranking-specific distractors (off-by-one errors).
    """
    options = {
        correct_value,
        correct_value + 1,
        correct_value - 1,
        correct_value + 2
    }
    return [o for o in options if o > 0]
def build_options(correct_value, unit, concept_type):

    if "Statistics" in concept_type or unit == "number" or unit == "fraction":

        correct_value = round(float(correct_value), 2)
        distractors = set()

        # Small controlled offsets (statistics-friendly)
        offsets = [0.5, 1, 1.5, 2]

        for o in offsets:
            distractors.add(round(correct_value + o, 2))
            distractors.add(round(correct_value - o, 2))

        # Remove invalid / negative
        distractors = {d for d in distractors if d >= 0}
        distractors.discard(correct_value)

        # Fallback if weak
        if len(distractors) < 3:
            distractors.update([
                round(correct_value * 0.9, 2),
                round(correct_value * 1.1, 2)
            ])

        distractors = list(distractors)[:3]

        options = [correct_value] + distractors
        random.shuffle(options)

        options = [f"{o}{' ' + unit if unit else ''}".strip() for o in options]
        correct_answer = f"{correct_value}{' ' + unit if unit else ''}".strip()

        return options, correct_answer
    
    if is_number(correct_value):
        correct_value = round(float(correct_value), 2)
        distractors = set()

        if "Percent" in concept_type or unit == "value":
            steps = [1, 1.5, 2, 2.5]
            for s in steps:
                distractors.add(round(correct_value + s, 2))
                distractors.add(round(correct_value - s, 2))
        else:
            multipliers = [0.6, 0.8, 1.2, 1.4]
            for m in multipliers:
                distractors.add(round(correct_value * m, 2))

        distractors.discard(correct_value)
        distractors = list(distractors)[:3]

        options = [correct_value] + distractors
        random.shuffle(options)

        options = [f"{o}{' ' + unit if unit else ''}".strip() for o in options]
        correct_answer = f"{correct_value}{' ' + unit if unit else ''}".strip()

        return options, correct_answer
    
    # correct_str = str(correct_value).strip()
    # distractors = config.LOGICAL_DISTRACTORS.get(correct_str, ["brother", "uncle", "cousin"])
    # random.shuffle(distractors)

    # options = [correct_str] + distractors[:3]
    # random.shuffle(options)

    # return options, correct_str


def select_template(concept, difficulty, last_used_template=None):
    templates = concept["templates"]
    if last_used_template and len(templates) > 1:
        available_templates = [t for t in templates if t != last_used_template]
    else:
        available_templates = templates[:]

    if difficulty == "easy":
        pool = available_templates[:max(1, len(available_templates) // 3)]

    elif difficulty == "medium":
        pool = available_templates[:max(2, len(available_templates) * 2 // 3)]

    else:
        pool = available_templates

    return random.choice(pool)

def save_question(questions):
    """
    Save one or multiple questions safely.
    """

    # Normalize input
    if isinstance(questions, dict):
        questions = [questions]

    if not isinstance(questions, list):
        raise ValueError("save_question expects dict or list of dicts")

    for question in questions:
        topic = question["topic"]
        concept_id = question["concept_id"]
        difficulty = question["difficulty"]

        # ---- Example storage path ----
        path = f"practice/data/question_bank/{topic}/{concept_id}/{difficulty}.json"

        os.makedirs(os.path.dirname(path), exist_ok=True)

        # ---- Load existing ----
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
        else:
            data = []

        # ---- Avoid duplicates ----
        existing_ids = {q["question_id"] for q in data}
        if question["question_id"] not in existing_ids:
            data.append(question)

        # ---- Save back ----
        with open(path, "w") as f:
            json.dump(data, f, indent=2)



def generate_params(concept, difficulty, role=None):
    params = {}

    difficulty = difficulty.lower().strip()  

    rules = concept.get("param_rules", {})
    if not rules:
        raise ValueError(f"No param_rules defined for concept")

    for param, rule in rules.items():
        if difficulty not in rule:
            raise ValueError(
                f"Difficulty '{difficulty}' not supported for param '{param}'. "
                f"Available: {list(rule.keys())}"
            )

        params[param] = random.choice(rule[difficulty])

    # Derived params (safe)
    if "distance_multiplier" in params and "speed" in params:
        params["distance"] = params["speed"] * params["distance_multiplier"]
        del params["distance_multiplier"]

    if not params:
        raise ValueError(
            f"generate_params produced empty params.\n"
            f"Concept rules: {rules}\n"
            f"Difficulty: {difficulty}"
        )

    return params



def parse_mcq_text(text):
    try:
        q_match = re.search(r"Question:\s*(.*?)\n\s*Options:", text, re.S)
        print(q_match)
        if not q_match:
            return None
        question = q_match.group(1).strip()

        options = {}
        for line in text.splitlines():
            line = line.strip()
            if re.match(r"^[A-D]\s*\)", line):
                key = line[0]
                options[key] = line.split(")", 1)[1].strip()

        if len(options) != 4:
            return None

        c_match = re.search(r"Correct option:\s*([A-D])", text)
        if not c_match:
            return None
        correct = c_match.group(1)

        e_match = re.search(r"Explanation:\s*(.*)", text, re.S)
        explanation = e_match.group(1).strip() if e_match else ""

        return {
            "question": question,
            "options": options,
            "correct_option": correct,
            "explanation": explanation
        }

    except Exception:
        return None

def plan_subtopics(subtopics, total, max_per_subtopic):
    plan = []
    counts = Counter()

    while len(plan) < total:
        s = random.choice(subtopics)
        if counts[s] < max_per_subtopic:
            plan.append(s)
            counts[s] += 1

    random.shuffle(plan)
    return plan


def split_mcq_blocks(text):
    if not text or not isinstance(text, str):
        return []
    blocks = []
    current = []
    for line in text.splitlines():
        if line.strip().startswith("Question:") and current:
            blocks.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))

    return blocks

    
    
    
def derive_params(concept_id, params):
    """
    Adds derived params ONLY if required by the concept.
    """

    # Arithmetic Series
    if concept_id == "LR_ARITHMETIC_SERIES":
        a, d = params["a"], params["d"]
        params.update({
            "a_plus_d": a + d,
            "a_plus_2d": a + 2*d,
            "a_plus_3d": a + 3*d
        })

    # Geometric Series
    elif concept_id == "LR_GEOMETRIC_SERIES":
        a, r = params["a"], params["r"]
        params.update({
            "a_times_r": a * r,
            "a_times_r2": a * (r ** 2),
            "a_times_r3": a * (r ** 3)
        })

    # Blood Relation → NO derived params
    # Coding-Decoding → NO derived params
    # Direction → NO derived params

    return params

# Global set for final-stage uniqueness
FINAL_QUESTION_HASHES = set()


def validate_question(
    question_text,
    options,
    correct_answer,
    concept_id,
    params
):
    """
    Final sanity + uniqueness checker.
    Works for ALL aptitude types.
    """

    #  Correct answer must be present
    if correct_answer not in options:
        return False

    #  Options must be unique
    if len(set(options)) != len(options):
        return False

    # Must have exactly 4 options
    if len(options) != 4:
        return False

    # Hash based on meaning, not wording
    try:
        signature = (
            concept_id,
            tuple(sorted(options)),
            correct_answer
        )
    except Exception:
        return False

    if signature in FINAL_QUESTION_HASHES:
        return False

    FINAL_QUESTION_HASHES.add(signature)
    if concept_id.startswith("STAT_"):

        try:
            correct_val = float(correct_answer.split()[0])
        except:
            return False

        # Probability bounds
        if "PROBABILITY" in concept_id:
            if not (0 <= correct_val <= 1):
                return False

        # Variance / Std Dev non-negative
        if "VARIANCE" in concept_id or "STD_DEV" in concept_id:
            if correct_val < 0:
                return False

        # Mean / Median must lie inside data range
        if "MEAN" in concept_id or "MEDIAN" in concept_id:
            values = params.get("values", [])
            if values:
                if not (min(values) <= correct_val <= max(values)):
                    return False

        # Mode must actually exist
        if "MODE" in concept_id:
            from collections import Counter
            values = params.get("values", [])
            if values:
                freq = Counter(values)
                if freq.most_common(1)[0][1] == 1:
                    return False
    if concept_id.startswith(("SI_", "CI_", "PL_", "TSD_", "TW_")):
        try:
            val = float(correct_answer.split()[0])
            if val < 0:
                return False
        except:
            pass

    return True


def validate_role_mcq(mcq):
    # Basic structure
    required_keys = {"question", "options", "correct_option", "dimension", "explanation"}
    if not required_keys.issubset(mcq):
        return False

    options = mcq["options"]

    # Exactly 4 options
    if len(options) != 4:
        return False

    # Correct option must exist
    if mcq["correct_option"] not in options:
        return False

    # Options must be unique
    if len(set(options.values())) != 4:
        return False

    # Avoid definition-style questions
    forbidden = ["what is", "define", "means", "refers to"]
    if any(word in mcq["question"].lower() for word in forbidden):
        return False

    return True


USE_LLM_PROBABILITY = 1.0
CHUNK_SIZE = 5

LAST_TEMPLATE_USED = {}
LLM_WORDING_CACHE = {}
QUESTION_COUNTER = {}

def get_last_template(user_id, concept_id):
    return LAST_TEMPLATE_USED.get((user_id, concept_id))

def set_last_template(user_id, concept_id, template):
    LAST_TEMPLATE_USED[(user_id, concept_id)] = template
    
def get_question_count(user_id, concept_id):
    return QUESTION_COUNTER.get((user_id, concept_id), 0)

def increment_question_count(user_id, concept_id):
    key = (user_id, concept_id)
    QUESTION_COUNTER[key] = QUESTION_COUNTER.get(key, 0) + 1

def get_chunk_index(user_id, concept_id):
    return get_question_count(user_id, concept_id) // CHUNK_SIZE



def is_complete_mcq(text):
    required = [
        "Question:",
        "Options:",
        "A)",
        "B)",
        "C)",
        "D)",
        "Correct option:",
        "Explanation"
    ]
    return all(r in text for r in required)



def is_empty_answer(answer: str) -> bool:
    return not answer or len(answer.strip()) < 5

def is_repeated_answer(answer: str, prev: str) -> bool:
    if not prev:
        return False
    return answer.strip().lower() == prev.strip().lower()


def safe_parse_json(text):
    try:
        return json.loads(text)
    except:
        return {"quality": "weak", "missing_points": []}



def handle_answer(state, answer: str):
    answer = answer.lower().strip()
    #  Explicit END intent
    if answer in [
        "quit", "exit", "stop", "end interview",
        "that's all", "done", "no more questions"
    ]:
        state['end_requested'] = True
        state['action'] = "END_INTERVIEW"
        # finalize_interview(state)
        return state

    #  Disengagement signals
    if answer in [
        "i dont know", "not sure", "no idea",
        "skip", "pass", "cannot say", "no answer"
    ]:
        state['disengagement_count'] += 1

        # If repeated disengagement → offer to end
        if state['disengagement_count'] >= 3:
            state['action'] = "CHANGE_TOPIC"
        else:
            state['action'] = "CHANGE_TOPIC"
        return state

    #  Normal answer
    state['disengagement_count'] = 0
    state['last_answer'] = answer
    return state




def load_topics(topic: str):

    topic = topic.lower().replace(" ", "_")

    base_dir = os.path.dirname(__file__)

    file_path = os.path.join(
        base_dir,
        "data",
        "question_bank",
        f"{topic}.json"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Topic '{topic}' not found")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_topic():
    return [f.replace(".json", "") for f in os.listdir(config.BASE_PATH) if f.endswith(".json")]


def get_aptitude_question(topic:str):
    data = load_topics(topic)
    q = random.choice(data)

    return {
        "id": q["id"],
        "question": q["question"],
        "options": q["options"],
        "difficulty": q["difficulty"],
        "concept_id": q["concept_id"]
    }


def normalize_number(val):
    """
    Extract numeric value from strings like:
    '120.5 currency', '3.5', '-26.0', '14.4'
    """
    if isinstance(val, (int, float)):
        return float(val)

    if isinstance(val, str):
        return float(val.split()[0])

    raise ValueError("Invalid numeric value")

def auto_verify_math_question(q,formula, tolerance=0.01):
    try:
        params = q["params"]
        options = q["options"]

        # compute true answer
        true_ans = FORMULA_REGISTRY[formula](**params)
        true_ans = float(true_ans)

        # CASE 1: options as LIST
        if isinstance(options, list):
            for opt in options:
                val = float(opt.split()[0])
                if abs(val - true_ans) <= tolerance:
                    q["correct_option"] = opt
                    q["explanation"] = f"Verified using {formula}"
                    return q

        # CASE 2: options as DICT
        elif isinstance(options, dict):
            for k, v in options.items():
                val = float(v.split()[0])
                if abs(val - true_ans) <= tolerance:
                    q["correct_option"] = k
                    q["explanation"] = f"Verified using {formula}"
                    return q

    except Exception:
        return None

    return None
def auto_verify_role_question(q):
    return (
        isinstance(q.get("question"), str)
        and len(q.get("options", {})) == 4
        and q["correct_option"] in q["options"]
        and q["question"].strip().endswith("?")
    )
    
    
