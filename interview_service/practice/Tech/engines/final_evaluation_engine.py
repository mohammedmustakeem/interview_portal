from openai import AsyncOpenAI
import json

class FinalReportEngine:

    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def generate(self, state):

        history = state.history or []
        
        if len(history) < 2:
            return {
        "overall_score":     f"{state.performance_score:.1f}/10",
        "candidate_level":   "insufficient_data",
        "strengths":         list(state.strong_topics or []),
        "weaknesses":        list(state.weak_topics or []),
        "topics_to_improve": list(state.weak_topics or []),
        "final_feedback":    (
            f"Only {len(history)} question(s) were answered. "
            "A minimum of 3 questions are required for a full report. "
            "Please attempt more questions for an accurate evaluation."
        )
        }
        
        history_text = "\n".join([
            f"Q: {h['question']}\nA: {h['answer']}\nQuality: {h['quality']}"
            for h in state.history
        ])
        
        prompt = f"""
        You are a senior technical interviewer writing a structured performance report.
        
        Candidate Role:    {state.role}
        Experience Level:  {state.experience}
        Difficulty:        {state.difficulty}
        Questions Asked:   {len(history)}
        Performance Score: {"numeric_score":.1f} / 10
        
        Strong Topics: {', '.join(state.strong_topics) if state.strong_topics else 'None identified'}
        Weak Topics:   {', '.join(state.weak_topics)   if state.weak_topics   else 'None identified'}
        
        Interview Transcript:
            {history_text}
        
            Instructions:
                - overall_score must be a number out of 10 (e.g. "7.2/10"), derived from the performance score and answer quality.
                - candidate_level must be one of: beginner, intermediate, strong
                - strengths: 2-4 specific strengths observed
                - weaknesses: 2-4 specific weaknesses observed
                - topics_to_improve: concrete topics the candidate should study
                - final_feedback: 2-3 sentences of honest, constructive feedback
        
                Return ONLY valid JSON — no markdown, no explanation:
        
            {{
                "overall_score":     "X.X/10",
                "candidate_level":   "beginner | intermediate | strong",
                "strengths":         ["...", "..."],
                "weaknesses":        ["...", "..."],
                "topics_to_improve": ["...", "..."],
                "final_feedback":    "..."
            }}
            """
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system","content":"You are a senior technical interviewer."},
                {"role":"user","content":prompt}
            ],
            temperature=0.2
        )
        raw = response.choices[0].message.content.strip()

        print("\n========== LLM RAW RESPONSE ==========")
        print(raw)
        print("======================================\n")
        import re
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        clean_json = match.group(0)
        if not match:
            raise ValueError(f"LLM did not return JSON:\n{raw}")
        try:
            return json.loads(clean_json)

        except Exception as e:
            print("Final report parsing failed:", e)
            print("RAW:", raw)
        
            return {
        "overall_score": state.performance_score,
        "candidate_level": "unknown",
        "strengths": state.strong_topics,
        "weaknesses": state.weak_topics,
        "topics_to_improve": state.weak_topics,
        "final_feedback": "Interview completed."
        }
