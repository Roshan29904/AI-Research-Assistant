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

