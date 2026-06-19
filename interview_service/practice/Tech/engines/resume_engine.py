import json
import re
import os
from pydantic import BaseModel, Field
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class ResumeProject(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    keywords: List[str] = []
    discussion_depth: int =  0 #ye btayega kitna deep jana hai
    discussed: bool =False #or it track ki cover ho gya ya nhi 


class ResumeSkill(BaseModel):
    name: str
    mentioned_in_projects: int = 0
    user_confidence_score: float = 0.5  # dynamic during interview
    verified: bool = False              # becomes true if user explains well

class ResumeData(BaseModel):
    skills: List[str] = []
    certifications: List[str] = []
    projects: List[ResumeProject] = []
    experience_years: float = 0.0
    
class ResumeIntelligence(BaseModel):

    # Core Resume Data
    projects: List[ResumeProject] = Field(default_factory=list)
    skills: List[ResumeSkill] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

    # Derived Intelligence
    strongest_skills: List[str] = Field(default_factory=list)
    weak_resume_areas: List[str] = Field(default_factory=list)

    # Runtime Tracking
    current_project: Optional[str] = None
    resume_drill_depth: int = 0
    mentioned_technologies: List[str] = Field(default_factory=list)
    challenged_technologies: List[str] = Field(default_factory=list)
    current_focus: Optional[str] = None
    
class ResumeParser:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

    def parse(self, resume_text: str, role) -> ResumeData:
        prompt = f"""Extract structured information from this resume and according to user role: {role} extract only similar content to {role} from resume and return ONLY valid JSON.
        
        Resume:
        {resume_text}
        
        Return this exact JSON structure:
        {{
          "skills": ["list of all technical skills, tools, languages, frameworks"],
          "certifications": ["list of certifications"],
          "experience_years": <total years as a float, 0.0 if not mentioned>,
          "projects": [
            {{
              "name": "project name",
              "description": "brief description",
              "technologies": ["tech used"],
              "keywords": ["relevant keywords"]
            }}
          ]
        }}
        
        Rules:
        - Include ALL technologies even if not mainstream
        - Infer experience_years from date ranges if not explicitly stated
        - Return 0.0 for experience_years if truly cannot be determined
        - Return empty arrays if section not found
        - No explanation, just JSON"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Parse this resume:\n\n{resume_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        raw = response.choices[0].message.content
        # strip markdown code fences if present
        raw = re.sub(r"^```(?:json)?\n?", "", raw.strip())
        raw = re.sub(r"\n?```$", "", raw.strip())
        data = json.loads(raw)

        projects = [ResumeProject(**p) for p in data.get("projects", [])]

        return ResumeData(
            skills=data.get("skills", []),
            certifications=data.get("certifications", []),
            experience_years=float(data.get("experience_years", 0.0)),
            projects=projects
        )

def to_resume_intelligence(resume_data: ResumeData) -> ResumeIntelligence:

    projects = [
        ResumeProject(
            name=p.name,
            description=p.description,
            technologies=p.technologies,
            keywords=p.keywords
        )
        for p in resume_data.projects
    ]

    skills = [
        ResumeSkill(name=s)
        for s in resume_data.skills
    ]

    return ResumeIntelligence(
        projects=projects,
        skills=skills,
        certifications=resume_data.certifications
    )
