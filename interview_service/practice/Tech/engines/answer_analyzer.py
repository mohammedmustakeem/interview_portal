from openai import AsyncOpenAI
import json
import re

from pydantic import BaseModel
from typing import List


class AnswerEvaluation(BaseModel):
    quality: str  # weak | medium | strong
    depth: str    # basic | intermediate | deep
    missing_points: List[str]
    score_delta: float
    
    
class AnswerAnalyzer:

    def __init__(self, client: AsyncOpenAI):
        self.client = client
        
    def _rule_based_check(self, answer: str):
        if not answer or len(answer.strip()) < 10:
            return AnswerEvaluation(
                quality="weak",
                depth="basic",
                missing_points=["Insufficient explanation"],
                score_delta=-1.0
            )
        if len(answer.split()) < 15:
            return AnswerEvaluation(
                quality="medium",
                depth="basic",
                missing_points=["Lacks detail"],
                score_delta=0.0
            )
        return None
    async def _llm_evaluate(self, state, answer: str):

        prompt = f"""
        Evaluate the candidate's answer.
        
        Question:
        {state.last_question}
        
        Answer:
        {answer}
        
        Evaluate:
        - Quality (weak, medium, strong)
        - Depth (basic, intermediate, deep)
        - Missing technical points
        - Score delta between -1 and +1
        
        Return ONLY JSON:
        
        {{
          "quality": "...",
          "depth": "...",
          "missing_points": ["..."],
          "score_delta": 0.0
        }}
        """

        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        raw = response.choices[0].message.content.strip()

        print("\n========== LLM RAW RESPONSE ==========")
        print(raw)
        print("======================================\n")

        # Extract JSON if model returned extra text
        match = re.search(r"\{.*\}", raw, re.DOTALL)

        if match:
            raw = match.group(0)

        try:
            parsed = json.loads(raw)
            return AnswerEvaluation(**parsed)

        except Exception as e:
            print("JSON Parse Error:", e)
            print("RAW RESPONSE:", raw)

        return AnswerEvaluation(
            quality="medium",
            depth="basic",
            missing_points=["LLM returned invalid JSON"],
            score_delta=0.0
        )
    
    async def analyze(self, state, answer: str):

        # Rule-based quick check
        rule_check = self._rule_based_check(answer)
        if rule_check:
            evaluation = rule_check
        else:
            evaluation = await self._llm_evaluate(state, answer)

        #  Update performance score
        state.performance_score = max(
            0,
            min(10, state.performance_score + evaluation.score_delta)
        )

        #  Update answer depth
        #state.answer_depth = evaluation.depth

        #  Update weak/strong topic tracking
        if evaluation.quality == "weak":
            if state.current_topic not in state.weak_topics:
                state.weak_topics.append(state.current_topic)

        if evaluation.quality == "strong":
            if state.current_topic not in state.strong_topics:
                state.strong_topics.append(state.current_topic)

        #  Store missing points
        #state.missing_points = evaluation.missing_points

        #  Store last answer
        state.last_answer = answer
        state.history.append({
            "question": state.last_question,
            "answer": answer,
            "quality": evaluation.quality,
            "depth": evaluation.depth,
            "topic": state.current_topic
        })
        return state
