import os
from practice.Config import config
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from practice.utils import is_complete_mcq
from langchain_core.messages import HumanMessage
from practice.Prompts.Aptitude_prompt import build_prompt_math, build_prompt_role

load_dotenv()

# llm = ChatMistralAI(
#     model=config.MODEL,
#     temperature=config.TEMPRATURE
# )
llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    temperature=0.5
)
# max_retries= 3

def generate_question_wording(base_question: str,sub_topic, difficulty: str):
    prompt = build_prompt_math(sub_topic, difficulty, base_question)
    
    response = llm.invoke([
        HumanMessage(content=prompt)
    ])
    
    return response.content.strip()

def generate_role_mcq_batch(category, difficulty, subtopics):
    
    prompt = build_prompt_role(category, difficulty, subtopics)
    MAX_RETRIES = 5

    for _ in range(MAX_RETRIES):
        text = llm.invoke(prompt).content
        if is_complete_mcq(text):
            return text   
    return None
