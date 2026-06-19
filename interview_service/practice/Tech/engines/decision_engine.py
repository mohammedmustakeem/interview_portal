import random
from enum import Enum
from practice.Tech.engines.interview_engine import InterviewEngineState

class QuestionType(Enum):
    RESUME_BASED = "resume_based"
    FUNDAMENTALS = "fundamentals"
    CHALLENGE = "challenge"
    SWITCH_TOPIC = "switch_topic"
    DEEP_DIVE = "deep_dive"
    SCENARIO = "scenario"
    COMFORT = "comfort"
    

class DecisionEngine:
    
    def decide_next_action(self, state: InterviewEngineState):
     
        confidence = state.confidence_score
        performance = state.performance_score
        weak_topics = state.weak_topics
        last_type = state.last_question_type
           
        if state.interview_phase in ["GREETING", "CONTEXT_SETUP"]:
            return QuestionType.RESUME_BASED
        
        if state.resume and state.total_questions == 0:
            return QuestionType.RESUME_BASED
        if state.topic_depth < 2:
            QuestionType.DEEP_DIVE
        if state.resume and state.total_questions < 3:
            return QuestionType.RESUME_BASED
    
        if confidence < 0.35:
            return QuestionType.COMFORT
    
        if performance < 3.0:
            return QuestionType.RESUME_BASED
    
        if performance < 4.5:
            return QuestionType.FUNDAMENTALS
    
        if performance > 7:
            return QuestionType.DEEP_DIVE
    
        if last_type == QuestionType.RESUME_BASED:
            return QuestionType.SCENARIO
    
        if weak_topics and state.total_questions > 5:
            return QuestionType.DEEP_DIVE
    
        return QuestionType.FUNDAMENTALS
         
         
    def adjust_difficulty(self, state:InterviewEngineState):
        
        performance = state.performance_score
        
        if performance <= 4:
            return "easy"
        elif performance <= 7:
            return "medium"
        else:
            return "hard"
        
        
    def decide(self, state:InterviewEngineState):
        question_type = self.decide_next_action(state)
        difficulty = self.adjust_difficulty(state)
        
        return {
            "question_type": question_type.value,
            "difficulty": difficulty
        }
        
        
    def select_next_topic(self, state:InterviewEngineState):
            covered = set(state.covered_topics or [])
            
            unused_primary = [t for t in (state.primary_topics or []) if t not in covered]
            if unused_primary:
                return random.choice(unused_primary)
    
            unused_secondary = [t for t in (state.secondary_topics or []) if t not in covered]
            if unused_secondary:
                return random.choice(unused_secondary)
    
            #Safe fallback — guard against empty list
            all_topics = (state.primary_topics or []) + (state.secondary_topics or [])
            if all_topics:
                print("All topics covered — recycling from full list.")
                return random.choice(all_topics)
    
            print("No topics available in session state.")
            return None
