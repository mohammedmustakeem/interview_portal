import re
import json
import asyncio
from typing import List
from pydantic import BaseModel, Field, field_validator
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

VALID_DIFFICULTIES = {"easy", "medium", "hard"}


class TopicTree(BaseModel):
    primary_topics: List[str] = Field(default_factory=list)  
    secondary_topics: List[str] = Field(default_factory=list)  

    @field_validator("primary_topics", "secondary_topics", mode="before")
    @classmethod
    def must_be_list(cls, v):
        """Ensure LLM doesn't return a string instead of list."""
        if isinstance(v, str):
            return [v]
        return v or []

def extract_json(text: str) -> dict:
    """
    Robust JSON extractor with 3-level fallback:
    1. ```json ... ``` block
    2. ``` ... ``` block  
    3. Raw text parse
    """
    # Level 1: ```json wrapper
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return json.loads(match.group(1))

    # Level 2: any code block
    match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    # Level 3: raw JSON
    return json.loads(text.strip())


class TopicEngine:

    SYSTEM_PROMPT = "You are a senior technical interviewer. Always respond with valid JSON only."

    def __init__(self, client: AsyncOpenAI):
        self.client = client

    def _validate_inputs(self, role: str, difficulty: str, experience: str):
        if not role.strip():
            raise ValueError("Role cannot be empty.")
        if difficulty.strip().lower() not in VALID_DIFFICULTIES:
            raise ValueError(f"Difficulty must be one of: {VALID_DIFFICULTIES}")
        if not experience.strip():
            raise ValueError("Experience cannot be empty.")

    def _build_prompt(self, role: str, difficulty: str, experience: str) -> str:
        return f"""Generate interview topics for a technical interview.
        Role: {role}
        Experience Level: {experience}
        Difficulty: {difficulty}
        
        Return ONLY this JSON structure, no extra text:
        {{
          "primary_topics": ["topic1", "topic2", "topic3", "topic4", "topic5", "topic6"],
          "secondary_topics": ["topic1", "topic2", "topic3", "topic4", "topic5", "topic6"]
        }}
        
        primary_topics: Core must-know topics for this role.
        secondary_topics: Good-to-know or advanced topics."""

    async def generate_topics(self, role: str, difficulty: str, experience: str) -> TopicTree:

        #  Validate before hitting the API
        self._validate_inputs(role, difficulty, experience)

        role = role.strip().title()
        difficulty = difficulty.strip().lower()
        experience = experience.strip().title()

        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": self._build_prompt(role, difficulty, experience)}
            ],
            temperature=0.3,
            response_format={"type": "json_object"},  # ✅ forces JSON, no markdown
        )

        raw_text = response.choices[0].message.content.strip()

        try:
            parsed = extract_json(raw_text)
            return TopicTree(**parsed)

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}\nRaw: {raw_text}")
            return TopicTree()

        except Exception as e:
            print(f" Unexpected error: {e}\nRaw: {raw_text}")
            return TopicTree()



# async def test():
#     client = AsyncOpenAI()
#     engine = TopicEngine(client)

#     result = await engine.generate_topics(
#         role="data science",
#         difficulty="easy",
#         experience="1 year"
#     )

#     print("Primary Topics:", result.primary_topics)
#     print("Secondary Topics:", result.secondary_topics)
#     print("Type:", type(result))


# if __name__ == "__main__":
#     asyncio.run(test())
