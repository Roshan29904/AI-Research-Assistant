from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState
from graph.router import planner_route
from graph.review_router import review_router

from agents.planner import planner_node
from agents.researcher import web_search_node, rag_research_node, both_research_node
from agents.synthesizer import synthesizer_node
from agents.reviewer import review_node 



graph = StateGraph(ResearchState)

graph.add_node("planner", planner_node)
graph.add_node("web_research", web_search_node)
graph.add_node("rag_research", rag_research_node)
graph.add_node("both_research", both_research_node)
graph.add_node("synthesizer", synthesizer_node)
graph.add_node("reviewer", review_node)

graph.add_edge(START, "planner")

graph.add_conditional_edges(
    "planner",
    planner_route,
    {
        "web_research": "web_research",
        "rag_research": "rag_research",
        "both_research": "both_research",
    },
)

graph.add_edge("web_research", "synthesizer")
graph.add_edge("rag_research", "synthesizer")
graph.add_edge("both_research", "synthesizer")
graph.add_edge("synthesizer", "reviewer")

graph.add_conditional_edges(
    "reviewer", review_router, {"final": END, "research_again": "planner"}
)

gra = graph.compile()