import random

class HRDecisionEngine:

    HR_TOPICS = [
        "introduction",
        "background",
        "strengths",
        "weaknesses",
        "failures",
        "teamwork",
        "conflict",
        "motivation",
        "career_goals",
        "company_fit"
    ]

    MAX_RESUME_QUESTIONS = 3

    def decide(self, state):

        decision = {
            "question_type": "behavioral",
            "topic": state.context_focus
        }
    
        # First question → intro
        if state.total_questions == 0:
            decision["question_type"] = "opening"
            return decision
    
        # Every 3rd question → resume
        if state.resume and state.total_questions % 3 == 0:
            decision["question_type"] = "resume_based"
            return decision
    
        # Short answer follow-up
        if state.last_answer and len(state.last_answer.split()) < 4:
            decision["question_type"] = "clarification"
            return decision
    
        return decision
    
    def _next_topic(self, current_topic):

        try:
            idx = self.HR_TOPICS.index(current_topic)
            return self.HR_TOPICS[idx + 1]
        except:
            return random.choice(self.HR_TOPICS)
