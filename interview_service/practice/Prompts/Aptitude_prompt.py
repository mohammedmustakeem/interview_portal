
def build_prompt_math(sub_topic,difficulty,base_question):
    prompt = f"""
You are a professional aptitude exam question rewriter.

Your task:
Rewrite the question into a different real-life scenario
related to the topic: {sub_topic}

CRITICAL RULES (MUST FOLLOW STRICTLY):
0.DO NOT REPEAT the same question in a different form. Each question must be unique in context and structure.
1. DO NOT change ANY numbers.
2. DO NOT change ANY mathematical values.
3. DO NOT modify placeholders like {{p}}, {{r}}, {{t}}, etc.
4. DO NOT replace placeholders with actual numbers.
5. DO NOT introduce new numbers.
6. DO NOT change the mathematical meaning.
7. DO NOT add explanation.
8. Output only ONE single question sentence.
9. Keep it exam-style and clear.
10. If placeholders exist, they MUST remain EXACTLY as written.
11. DO NOT use the same real-life scenario as the original question. For example, if the original question is about a train, do not use a train in the rewritten question.
Difficulty level: {difficulty}

Original Question:
{base_question}

Return ONLY the rewritten question.
"""
    return prompt

def build_prompt_role(category, subtopics, difficulty):
    prompt = f"""
    Generate ONE aptitude MCQ.
    
    Category: {category}
    Subtopic: {subtopics}
    Difficulty: {difficulty}
    if category is data-interpretation only give theorytical questions
    and please give correct options and answer of the questions 
    STRICT RULES:
    - Exactly ONE question
    - Exactly 4 options A,B,C,D
    - Exactly ONE correct option
    - NO truncation
    - NO extra text
    - If you cannot complete, DO NOT answer
    
    FORMAT (EXACT):
    
    Question:
    <text>
    
    Options:
    A) <text>
    B) <text>
    C) <text>
    D) <text>
    
    Correct option: A/B/C/D
    
    Explanation:
    <1-2 lines>
    """
    
    return prompt
