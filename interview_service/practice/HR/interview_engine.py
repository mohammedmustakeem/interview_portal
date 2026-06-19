import uuid
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from practice.Config import config
from practice.Prompts.HR_prompt import build_prompt, build_hr_prompt, build_hr_prompt_early_exit
from practice.Tech.engines.resume_engine import ResumeIntelligence
import warnings
import datetime

warnings.filterwarnings("ignore")

# DATA MODELS
load_dotenv()


class Message(BaseModel):
    role: Literal["hr", "candidate"]
    content: str



class HRInterviewState(BaseModel):

    session_id: str
    user_id: Optional[str] = None

    role: str
    experience: str

    # Conversation memory
    last_question: Optional[str] = None
    last_answer: Optional[str] = None
    last_reaction: Optional[str] = None

    # Interview flow
    interview_phase: str = "GREETING"
    current_topic: Optional[str] = "introduction"

    # Tracking metrics
    total_questions: int = 0
    followup_count: int = 0
    topic_question_count: int = 0

    # Candidate behaviour
    interruption_count: int = 0
    disengagement_count: int = 0
    end_requested: bool = False

    # Candidate evaluation
    communication_score: float = 0.0
    confidence_score: float = 0.5
    hr_score: float = 0

    # Observations
    strong_points: List[str] = Field(default_factory=list)
    weak_points: List[str] = Field(default_factory=list)

    discussed_projects: List[str] = Field(default_factory=list)

    # Conversation history
    history: List[dict] = Field(default_factory=list)

    resume: Optional[ResumeIntelligence] = None
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    

MAX_CONTEXT_QUESTIONS = 2

# STAGE FLOW (SYSTEM GUARDED)
STAGE_ORDER = [
    "intro",
    "background",
    "strengths",
    "failure",
    "company_fit",
    "closing"
]

def next_stage(stage: str) -> str:
    if stage == "closing":
        return "done"
    return STAGE_ORDER[STAGE_ORDER.index(stage) + 1]


# LLM
# llm = ChatMistralAI(
#     model="mistral-small-latest",
#     temperature=0.4
# )

def normalize_llm_output(output):
    if isinstance(output, str):
        return output
    if isinstance(output, list):
        return " ".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in output
        )
    return str(output)

llm = ChatOpenAI(
    model=config.MODEL,
    temperature=0.2
)  

# HR QUESTION GENERATOR
def generate_hr_question(state: HRInterviewState) -> str:
    prompt = build_prompt(
        state=state,
        role=state.role,
        experience=state.experience,
        stage=state.stage,
        conversation=state.messages,
        context_focus=state.context_focus,
        context_question_count=state.context_question_count
    )
    response = llm.invoke(prompt)

    content = response.content

    # Normalize output (CRITICAL FIX)
    if isinstance(content, list):
        content = " ".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )

    return str(content)

# INTERVIEW ENGINE (ONE TURN)
def interview_step(state: HRInterviewState) -> HRInterviewState:

    if state.stage == "done":
        state.active = False
        return state

    question = generate_hr_question(state)
    

    state.messages.append(
        Message(role="hr", content=question)
    )

    #  stage moves ONLY after HR asks
    #state.stage = next_stage(state.stage)
    
    
    state.context_question_count += 1
    if state.context_question_count >= MAX_CONTEXT_QUESTIONS:
        state.context_focus = next_stage(state.context_focus)
        state.context_question_count = 0
    if state.stage == "done":
        state.active = False

    return state


# SESSION START
def start_interview(role: str, experience: str) -> HRInterviewState:
    return HRInterviewState(
        session_id=str(uuid.uuid4()),
        role=role,
        experience=experience,
        stage="intro",
        messages=[],
        active=True,
        context_focus=STAGE_ORDER[0],
        context_question_count=0
    )


def finalize_hr_interview(answers:List, questions:List, question_count:int):
    if question_count < 4:
        prompt = build_hr_prompt_early_exit(answers,questions, question_count)
    else:
        prompt = build_hr_prompt(answers, questions, question_count)
    response = llm.invoke(prompt)
    question = normalize_llm_output(response.content)
    return question



def run_hr_round(role, experience):
    print("\n HR Interview Started\n")

    # Interview start
    question_count = 0
    state = start_interview(role=role, experience=experience)
    answers = []
    questions = []
    while state.active:
        
        # HR asks question
        state = interview_step(state)
        print(f"\nHR: {state.messages[-1].content}")
        question_count += 1
        questions.append(state.messages[-1].content)
        #vision.start()
        # If interview finished internally
        if not state.active:
            print("\n Interview completed.")
            break

        # User answering phase
        answer = input("You: ").strip()
        answers.append(answer)
        state.messages.append(
            Message(role="candidate", content=answer)
        )

        state.last_answer = answer
        # Candidate exits manually
        if answer.lower() in ["exit", "quit", "done"]:
            print("\n Interview ended by candidate.")
            finalize_hr_interview(answers,questions,question_count)
            return
        
    # Interview end
    # Final HR summary (scores + tips)
    finalize_hr_interview(answers,questions,question_count)
    

# run_hr_round("Backend developer", "junior 1-2")
