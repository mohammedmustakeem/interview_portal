import uuid
import datetime
import warnings
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from practice.HR.interview_state import HRInterviewState, Message
from practice.Prompts.HR_prompt import *
from practice.HR.decision_engine import HRDecisionEngine
from practice.Tech.engines.resume_engine import *
from practice.Tech.engines.pdf_reader import *

import random

warnings.filterwarnings("ignore")
load_dotenv()

class _Config:
    MODEL: str = "llama-3.3-70b-versatile"          # change to your model string

config = _Config()


STAGE_ORDER: List[str] = [
    "intro",
    "background",
    "strengths",
    "failure",
    "company_fit",
    "closing",
]
MAX_CONTEXT_QUESTIONS = 2   # how many questions per topic before moving on


def next_stage(stage: str) -> str:
    if stage in ("closing", "done"):
        return "done"
    try:
        idx = STAGE_ORDER.index(stage)
    except ValueError:
        return "done"
    return STAGE_ORDER[idx + 1] if idx + 1 < len(STAGE_ORDER) else "done"


llm = ChatOpenAI(
    model=config.MODEL,
    temperature=0.2,
)


def normalize_llm_output(output) -> str:
    if isinstance(output, str):
        return output
    if isinstance(output, list):
        return " ".join(
    item.get("text", "") if isinstance(item, dict) else str(item)
    for item in output
    )
    return str(output)

decision_engine = HRDecisionEngine()

def generate_hr_question(state: HRInterviewState) -> str:

    decision = decision_engine.decide(state)

    selected_item = None
    resume_focus = None

    # Resume-aware question selection
    if decision["question_type"] == "resume_based" and state.resume:

        # Priority: project → skill → education
        if state.resume.projects:

            available = [
                p for p in state.resume.projects
                if p.name not in state.discussed_projects
            ]

            if not available:
                available = state.resume.projects

            selected_item = random.choice(available)
            resume_focus = "project"
            state.discussed_projects.append(selected_item.name)

        elif state.resume.skills:
            selected_item = random.choice(state.resume.skills)
            resume_focus = "skill"
        elif state.resume.education:
            selected_item = random.choice(state.resume.education)
            resume_focus = "education"
            
    prompt = build_prompt(
        state=state,
        decision=decision,
        selected_item=selected_item,
        resume_focus=resume_focus
    )
    response = llm.invoke(prompt)
    
    return normalize_llm_output(response.content).strip()


def interview_step(state: HRInterviewState) -> HRInterviewState:
    """Generate the next HR question, append it, and advance topic tracking."""
    if state.stage == "done":
        state.active = False
        return state

    question = generate_hr_question(state)

    # Pydantic-safe list mutation: reassign instead of in-place append
    state.messages = state.messages + [Message(role="hr", content=question)]
    state.last_question = question
    state.total_questions += 1

    # Advance topic focus after MAX_CONTEXT_QUESTIONS
    new_count = state.context_question_count + 1
    if new_count >= MAX_CONTEXT_QUESTIONS:
        next_focus = next_stage(state.context_focus)
        state.context_focus = next_focus
        state.context_question_count = 0
        if next_focus == "done":
            state.stage = "closing"
    else:
        state.context_question_count = new_count
        
    state.updated_at = datetime.datetime.utcnow()
    return state


def record_candidate_answer(state: HRInterviewState, answer: str) -> HRInterviewState:
    """Append the candidate's answer and update short-term memory."""
    state.messages = state.messages + [Message(role="candidate", content=answer)]
    state.last_answer = answer
    state.updated_at = datetime.datetime.utcnow()
    return state


def start_interview(role: str, experience: str) -> HRInterviewState:
    return HRInterviewState(
session_id=str(uuid.uuid4()),
role=role,
experience=experience,
stage=STAGE_ORDER[0],
context_focus=STAGE_ORDER[0],
)


def finalize_hr_interview(
    answers: List[str], questions: List[str], question_count: int
) -> str:
    if question_count < 4:
        prompt = build_hr_prompt_early_exit(answers, questions, question_count)
    else:
        prompt = hr_finalize_prompt(answers, questions, question_count)

    response = llm.invoke(prompt)
    return normalize_llm_output(response.content)

EXIT_COMMANDS = {"exit", "quit", "done", "bye", "end"}


def run_hr_round(role: str, experience: str, resume_path: str | None = None) -> None:
    print("\n" + "=" * 55)
    print("   HR Mock Interview — Synclyft")
    print("=" * 55)
    print(f"   Role       : {role}")
    print(f"   Experience : {experience}")  
    print("   Type 'exit' at any time to end the interview.")
    print("=" * 55 + "\n")

    state = start_interview(role=role, experience=experience)
    questions: List[str] = []
    answers: List[str] = []
    if resume_path:
        
        print("Parsing resume...")
        text = PDFTextExtractor.extract_text(resume_path)
    
        parser = ResumeParser()
        resume_data = parser.parse(text, role)
    
        resume_intel = to_resume_intelligence(resume_data)
        state.resume = resume_intel
    
        print("Resume parsed successfully.")
        print("Projects found:", [p.name for p in resume_intel.projects])
        
        
    while state.active:
        # ── HR asks ──────────────────────────────────────
        state = interview_step(state)
        hr_message = state.messages[-1].content
        print(f"\nInterviewer : {hr_message}\n")
        questions.append(hr_message)

        # Graceful close: if we reached closing stage and just asked the
        # farewell question, we're done collecting answers.
        if state.stage == "closing" and state.context_focus == "done":
            state.active = False
            break

        # ── Candidate answers ────────────────────────────
        try:
            answer = input("You   : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n[Interview interrupted]")
            answer = ""

        if answer.lower() in EXIT_COMMANDS or not answer:
            print("\nInterview ended by candidate.\n")
            answers.append(answer or "(no answer)")
            break
        answers.append(answer)
        state = record_candidate_answer(state, answer)
        # ── Final evaluation ─────────────────────────────────
    print("\n" + "=" * 55)
    print("   Interview Feedback")
    print("=" * 55 + "\n")
    feedback = finalize_hr_interview(answers, questions, len(questions))
    print(feedback)
    print("\n" + "=" * 55 + "\n")
  
# if __name__ == "__main__":
#     run_hr_round("Data Science", "Junior (0–1 years)", "practice\Tech\Thasin_Resume.pdf")
    
