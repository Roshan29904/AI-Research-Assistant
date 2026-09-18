from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from config import model
from graph.state import ResearchState
from prompts.planner import PLANNER


class PlannerOutput(BaseModel):
    route: Literal["WEB", "RAG", "BOTH"] = Field(description="Route selected for answering the user query.")


planner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PLANNER),
        ("human", "{query}"),
    ]
)

planner_chain = planner_prompt | model


def planner_node(state: ResearchState):
    """Decide whether the graph should use web, rag, or both sources."""
    result = planner_chain.invoke({"query": state["query"]})
    route = str(getattr(result, "content", result)).strip().upper()

    if route not in {"WEB", "RAG", "BOTH"}:
        normalized = route.lower()
        if "rag" in normalized and "web" in normalized:
            route = "BOTH"
        elif "rag" in normalized:
            route = "RAG"
        else:
            route = "WEB"

    return {"route": route}
