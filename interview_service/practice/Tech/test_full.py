import asyncio
from openai import AsyncOpenAI
import os
from practice.Tech.engines.topic_engine import TopicEngine
from practice.Tech.Question_generator import QuestionGenerator
from practice.Tech.engines.answer_analyzer import AnswerAnalyzer
from practice.Tech.engines.decision_engine import DecisionEngine
from practice.Tech.engines.personality_engine import PersonalityEngine
from practice.Tech.engines.interview_engine import InterviewEngineState

async def run_interview():

    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    topic_engine = TopicEngine(client)
    question_engine = QuestionGenerator(client)
    analyzer = AnswerAnalyzer(client)
    decision_engine = DecisionEngine()
    personality_engine = PersonalityEngine()

    role = "Data Science"
    experience = "1 year"
    difficulty = "hard"

    topics = await topic_engine.generate_topics(role, difficulty, experience)

    state = InterviewEngineState(
        session_id="test124",
        user_id="user2",
        role=role,
        experience=experience,
        difficulty=difficulty,
        primary_topics=topics.primary_topics,
        secondary_topics=topics.secondary_topics,
        current_topic=topics.primary_topics[0] if topics.primary_topics else None,
        personality_mode="strict"
    )

    print("\nInterview Started")
    print("Primary Topics:", state.primary_topics)
    print("------------------------------------------------")

    for _ in range(10): 

        decision = decision_engine.decide(state)

        if state.topic_question_count >= 3:
            state.covered_topics.append(state.current_topic)
            state.current_topic = decision_engine.select_next_topic(state)
            state.topic_question_count = 0

        personality_prompt = personality_engine.build_prompt(
            state.personality_mode
        )

        generated = await question_engine.generate(
            state,
            decision,
            personality_prompt
        )

        print(f"\n Interviewer ({decision['question_type']}):")
        print(generated.question)

        # Update state
        state.last_question = generated.question
        state.last_question_type = decision["question_type"]
        state.topic_question_count += 1
        state.total_questions += 1

        user_answer = input("\n Your Answer: ").strip()

        state = await analyzer.analyze(state, user_answer)
        reac = await reaction.generate_feedback(state)
        print("Interviwer: ", reac)
        # Debug output
        print("\n Performance Score:", state.performance_score)
        print(" Current Topic:", state.current_topic)
        print(" Weak Topics:", state.weak_topics)
        print(" Strong Topics:", state.strong_topics)
        print("------------------------------------------------")

    print("\n Interview Finished")


if __name__ == "__main__":
    asyncio.run(run_interview())
