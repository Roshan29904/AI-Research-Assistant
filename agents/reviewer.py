from langchain_core.prompts import ChatPromptTemplate

from config import model
from graph.state import ResearchState
from prompts.reviewer import HUMAN, REVIEWER


review_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", REVIEWER),
        ("human", HUMAN),
    ]
)

chain = review_prompt | model


def review_node(state: ResearchState):
    result = chain.invoke({
        "query": state["query"],
        "draft": state["draft"],
    })
    feedback = str(getattr(result, "content", result)).strip()
    decision = "Pass" if "pass" in feedback.lower() else "Fail"
    current_revision = int(state.get("revision_number", 0))

    return {
        "review": feedback,
        "review_passed": decision == "Pass",
        "revision_number": current_revision + 1,
    }