# from langgraph.graph import StateGraph, START, END
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from typing import TypedDict, Annotated
# from langchain_core.messages import SystemMessage,HumanMessage
# from langgraph.graph.message import add_messages
# from practice.Config import config
# load_dotenv()


# #Remember this ai also have contain memory so it can tell feedback according to prevoius performance,


# model = ChatOpenAI(model = config.MODEL, temperature=config.ANALYSIS_TEMPERATURE)

# system_prompt = SystemMessage(
#         content=config.SYSTEM_PROMPT
#     )
# human_prompt = HumanMessage(
#             content=config.HUMAN_PROMPT
#         )
    
# class AnalysisState(TypedDict):
#     message: Annotated[list, add_messages]
    

# def analysis_node(state:AnalysisState):
#     #it will take data from json file and pass it to the model
#     messages = [system_prompt, human_prompt]
#     response = model.invoke(messages)
    
#     return {'message': response}

    
# graph = StateGraph(AnalysisState)
# graph.add_node("analysis", analysis_node)
# graph.add_edge(START, "analysis")
# graph.add_edge("analysis", END)
# analysis_graph = graph.compile()

# # ---------------- RUN ----------------
# def Analyze_performance():
#     print("\n --- Analyzing Performance ---\n")
    
#     result = analysis_graph.invoke({
#         "message": [
#             HumanMessage(content = config.INVOKE_PROMPT)
#         ]
#     })
    
#     print("\n AI-Generated Feedback:\n")
#     return result["message"][-1].content
