from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from config import model
from graph.state import ResearchState
from prompts.reviewer import REVIEWER, HUMAN

class ReviewOutput(BaseModel):
    decision: Literal["Pass", "Fail"] = Field(description="Is the report acceptable")
    feedback: str = Field(description="Feedback for imporving the report.")


review_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", REVIEWER),
        ("human", HUMAN)
    ]
)

chain = review_prompt | model.with_structured_output(ReviewOutput())



def review_node(state: ResearchState):
    result = chain.invoke({
        "query": state["query"],
        "draft": state["draft"],
        
    })
    return result

