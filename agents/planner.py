from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from config import model
from graph.state import ResearchState
from prompts.planner import PLANNER

class PlannerOutput(BaseModel):
    route: Literal["WEB", "RAG", "BOTH"] = Field(description="Route selected for answering the user query.")
    



planner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PLANNER),
        ("human", "{query}")
    ]
)


    
Planner_llm = model.with_structured_output(PlannerOutput)

planner_chain = planner_prompt | Planner_llm




def planner_node(state: ResearchState):
    """decide the flow of the graph, whether the route should be WEB , RAG or BOTH"""
    result = planner_chain.invoke({
        "query": state["query"]
    })
    route = {"route": result.route}
    return route