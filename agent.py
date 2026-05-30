from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from tools.application_tools import open_applications , check_opened_applications
from tools.browser_tools import browser_navigate , browser_click , browser_type , browser_press_key , browser_screenshot
import json , os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GORK_API_LLAMA_3_70B_VERSATILE")


llm  = ChatGroq(model="llama-3.3-70b-versatile", temperature=0 , api_key=key)


# temp context passing and memory
class State (TypedDict):
    agent: str
    task: dict
    message : str
    application_name : str
    route: str


# node to open application witin the system
def applications(state : State):
    application_name = state["application_name"]
    result = open_applications.invoke({"application_name": application_name})
    return {
        "agent": "applications",
        "task": state["task"],
        "message": result,
        "application_name": application_name
    }

# node for the browser , contains all the tools that are needed for browser operation 
def browser(state : State):
    query = state["application_name"]
    # If it looks like a URL, navigate directly; otherwise search Google
    if query.startswith("http") or "." in query and " " not in query:
        url = query if query.startswith("http") else f"https://{query}"
    else:
        url = f"https://www.google.com/search?q={query}"

    browser_navigate.invoke({"url": url})
    browser_screenshot.invoke({"path": "workspace"})
    return {    
        "agent": "browser",
        "task": state["task"],
        "message": f"Opened {url} in Brave",
        "application_name": state["application_name"]
    }

# used to route the applciation 
def router(state:State):
    response = llm.invoke(
        [
            SystemMessage(content='Reply ONLY with JSON: {"type":"app" or "browser","name":"<lowercase name or search query>"}. Apps: notepad,calculator,paint,word,excel,spotify,vlc,discord,teams,brave,chrome,edge,firefox. If the user wants to search or browse something online, set type to "browser" and set name to the full search query (e.g. "cat pics"). If they want to open a specific website, set name to the URL.'),
            HumanMessage(content=state['task'])
        ]
    )

    try:
        parsed = json.loads(response.content.strip())
        route = parsed["type"]
        application_name = parsed["name"]
    except (json.JSONDecodeError, KeyError):
        route = "app"
        application_name = response.content.strip().lower()

    print(f"FROM ROUTER --> {route}: {application_name}")
    return {"application_name": application_name, "route": route}


def route_decision(state: State) -> str:
    """Conditional edge: route to 'applications' or 'browser'."""
    return "browser" if state.get("route") == "browser" else "applications"


workflow = StateGraph(State)
# adding nodes , nothing but the tools so the graph can access the tools 
workflow.add_node("router" , router)
workflow.add_node("applications" , applications)
workflow.add_node("browser" , browser)


# edge is the flow on how the agent will be executed
workflow.add_edge(START, "router")
workflow.add_conditional_edges("router", route_decision, {"applications": "applications", "browser": "browser"})
workflow.add_edge("applications" , END)
workflow.add_edge("browser" , END)
graph = workflow.compile()

if __name__ == "__main__":
    UserMessage = input("how can i help ? :")


    initial_state = {
        "agent": "router",
        "task": UserMessage,
        "message": "",
        "application_name": "",
        "route": ""
    }
    print("BEFORE -->", initial_state)
    result = graph.invoke(initial_state)
    print("AFTER -->", result)
