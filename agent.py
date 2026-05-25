from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from tools.application_tools import open_applications , check_opened_applications
import json , os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GORK_API_LLAMA_3_70B_VERSATILE")


llm  = ChatGroq(model="llama-3.3-70b-versatile", temperature=0 , api_key=key)


class State (TypedDict):
    agent: str
    task: dict
    message : str
    application_name : str


def applications(state : State):
    application_name = state["application_name"]
    result = open_applications.invoke({"application_name": application_name})
    return {
        "agent": "applications",
        "task": state["task"],
        "message": result,
        "application_name": application_name
    }

# used to route the applciation 
def router(state:State):
    response = llm.invoke(
        [
            SystemMessage(content="Extract the application name from the user's request. Respond with ONLY the application name in lowercase, nothing else. Examples: notepad, brave, chrome, spotify, vlc"), 
            HumanMessage(content=state['task'])
        ]
    )

    application_name = response.content.strip().lower()
    print("FROM ROUTER -->", application_name)
    return {"application_name": application_name}


workflow = StateGraph(State)
# adding nodes , nothing but the tools so the graph can access the tools 
workflow.add_node("router" , router)
workflow.add_node("applications" , applications)


# edge is the flow on how the agent will be executed
workflow.add_edge(START, "router")
workflow.add_edge("router" , "applications")

graph = workflow.compile()

if __name__ == "__main__":
    UserMessage = input("how can i help ? :")


    initial_state = {
        "agent": "router",
        "task": UserMessage,
        "message": "",
        "application_name": ""
    }
    print("BEFORE -->", initial_state)
    result = graph.invoke(initial_state)
    print("AFTER -->", result)
