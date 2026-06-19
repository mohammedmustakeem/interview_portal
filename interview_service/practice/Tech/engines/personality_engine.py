from enum import Enum 

class PersonalityMode(str, Enum):
    FRIENDLY = "friendly"
    STRICT = "strict"
    FAANG = "faang"
    STARTUP = "startup"
    
    
class PersonalityProfile:
    def __init__(self, tone, probing_style, encouragement, depth_focus):
        self.tone = tone
        self.probing_style = probing_style
        self.encouragement = encouragement
        self.depth_focus = depth_focus
        
    
    
class PersonalityEngine:
    def __init__(self):
        self._profiles = {
            PersonalityMode.FRIENDLY: PersonalityProfile(
                tone="Warm, conversational, supportive.",
                probing_style="Gentle follow-up questions.",
                encouragement="Provide encouragement when needed.",
                depth_focus="Moderate depth, focus on clarity."
            ),
            PersonalityMode.STRICT: PersonalityProfile(
                tone="Professional, concise, direct.",
                probing_style="Precise and technical probing.",
                encouragement="Minimal encouragement.",
                depth_focus="High technical accuracy required."
            ),
            PersonalityMode.FAANG: PersonalityProfile(
                tone="Senior FAANG interviewer style.",
                probing_style="Deep trade-off and optimization probing.",
                encouragement="Neutral tone.",
                depth_focus="Very deep technical reasoning."
            ),
            PersonalityMode.STARTUP: PersonalityProfile(
                tone="Fast-paced, practical CTO style.",
                probing_style="Real-world implementation focused.",
                encouragement="Direct but motivating.",
                depth_focus="Scalability and production focus."
            )
        }
        
        
    def build_prompt(self, mode:PersonalityMode):
        profile = self._profiles.get(mode, self._profiles[PersonalityMode.FRIENDLY])
        return  f"""
        Interviewer Personality Instructions:
        - Tone: {profile.tone}
        - Probing Style: {profile.probing_style}
        - Encouragement Style: {profile.encouragement}
        - Depth Expectation: {profile.depth_focus}
        Maintain consistency with this personality.
        """
        
    
    def adjust_for_candidate(self, mode:PersonalityMode, confidence: float):
        base_prompt = self.build_prompt(mode)
        
        if confidence < 0.4:
            return base_prompt + "\nBe slightly more supportive due to low confidence."

        return base_prompt
    
    
