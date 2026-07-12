from typing import Literal
from graph.state import ResearchState


def planner_route(state: ResearchState) -> Literal["web_research", "rag_research", "both_research"]:
    """it reads the planner's output and returns the next node in the graph"""
    route = state["route"]
    if route =="WEB":
        return "web_research"
    elif route == "RAG":
        return "rag_research"
    else:
        return "both_research"
    
    
