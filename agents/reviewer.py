from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from config import model
from graph.state import ResearchState
from prompts.reviewer import REVIEWER, HUMAN
from typing import Literal


class ReviewOutput(BaseModel):
    decision: Literal["Pass", "Fail"] = Field(description="Is the report acceptable")
    feedback: str = Field(description="Feedback for improving the report.")


parser = PydanticOutputParser(pydantic_object=ReviewOutput)

review_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", REVIEWER + "\n\n{format_instructions}"),
        ("human", HUMAN),
    ]
).partial(format_instructions=parser.get_format_instructions())

chain = review_prompt | model | parser


def review_node(state: ResearchState):
    result = chain.invoke({
        "query": state["query"],
        "draft": state["draft"],
    })

    return {
        "review": result.feedback,
        "review_passed": result.decision == "Pass",
    }