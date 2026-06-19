import random
from practice.utils import (
    generate_params,
    param_signature,
    is_new_question,
    register_question,
    derive_params,
    select_template,
    is_number,build_options,get_chunk_index,get_last_template,set_last_template,LLM_WORDING_CACHE,increment_question_count, auto_verify_math_question
)
from practice.Aptitude.formula_engine.load_formula import compute_answer
from practice.Aptitude.wording_llm import generate_question_wording
from practice.Aptitude.registory import CONCEPT_REGISTORY

def build_question(
    concept_id: str,
    difficulty: str,
    user_id: str,
    user_role: str,
    user_type: str,
    user_topic: str
):
    """
    Builds ONE unique aptitude question (Arithmetic / Stats / DI / LR).
    """

    if concept_id not in CONCEPT_REGISTORY:
        raise ValueError(f"Unknown concept_id: {concept_id}")

    concept = CONCEPT_REGISTORY[concept_id]
    MAX_TRIES = 15
    for _ in range(MAX_TRIES):

        # 1 Generate parameters
        params = generate_params(
            concept=concept,
            difficulty=difficulty,
            role=user_role
        )
        params = derive_params(concept_id, params)
        params = {
            k: v for k, v in params.items()
            if k in concept["params"]
        }
        if concept["formula"] in {
                "principal_from_si",
                "rate_from_si",
                "time_from_si"
            }:
                known_params = {
                    k: v for k, v in params.items()
                    if k in concept["params"]
                }
        
                result = compute_answer(
                    concept["formula"],
                    **known_params
                )
        
                # Inject missing variable into params
                for key in concept["params"]:
                    if key not in params:
                        params[key] = round(result, 2)
                        break
            
        # 2️ Uniqueness check
        params = dict(sorted(params.items()))

        signature_params = {
                k: params[k]
                for k in concept["params"]
            }

        signature = param_signature(concept_id, signature_params)
        
        
        if not is_new_question(user_id, concept_id, signature):
            continue
        register_question(user_id, concept_id, signature)

        # 3️ Template + wording
        last_template = get_last_template(user_id, concept_id)

        template = select_template(
            concept=concept,
            difficulty=difficulty,
            last_used_template=last_template
        )
        
        set_last_template(user_id, concept_id, template)
        
        base_question = template.format(**params)
        increment_question_count(user_id, concept_id)
        chunk_index = get_chunk_index(user_id, concept_id)
        
        cache_key = (user_id, concept_id, base_question)
        
        #print("Base questions:", base_question)
        
        if cache_key not in LLM_WORDING_CACHE:
            try:
                question_text = generate_question_wording(
                    base_question=base_question,
                    sub_topic=concept["sub_topic"],
                    difficulty=difficulty
                )
                LLM_WORDING_CACHE[cache_key] = [question_text]
                #print("LLM USED for chunk:", chunk_index)
        
            except Exception:
                #print("LLM fail → fallback")
                LLM_WORDING_CACHE[cache_key] = [base_question]
        question_text = random.choice(LLM_WORDING_CACHE[cache_key])
        if any(f"{{{k}}}" not in question_text for k in params.keys()):
              question_text = base_question
        

        #question_text = question_text.format(**params)
        # 4️ Compute correct answer
        base_params = {
            k: v for k, v in params.items()
            if k in concept["params"]
        }

        try:
            correct_value = compute_answer(
                concept["formula"],
                **base_params
            )
        except Exception:
            continue
        if correct_value is None:
            continue
        display_value = (
            round(correct_value, 2)
            if is_number(correct_value)
            else correct_value
        )
        if '{' in question_text:
            question_text = base_question
        
        # print("question_text: ",question_text)
        unit = concept.get("unit", "")
        #Solve this error kaal 
        options, correct_answer = build_options(
            display_value,
            unit,
            concept["topic"]
        )
        candidate = {
    "question": question_text,
    "options": options,
    "correct_option": correct_answer,
    "concept_id": concept_id,
    "params": params,
    }

# AUTO VERIFY USING FORMULA
        formula_name = concept['formula']
        if not auto_verify_math_question(candidate, formula_name):
            continue
        # print(options)
        # print("correct_value",correct_answer)
        
        return {
            "question_id": f"{concept_id}_{signature[:8]}",
            "concept_id": concept_id,
            "topic": concept["topic"],
            "difficulty": difficulty,
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "params": params,
            "meta": {
                "formula": concept["formula"],
                "unit": unit,
                "type": user_type
            },
            "topic":user_topic
        }

    # EXHAUSTED
    return {
        "status": "EXHAUSTED",
        "message": f"No new questions available for concept '{concept_id}'"
    }


