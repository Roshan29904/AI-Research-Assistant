from langchain_core.prompts import ChatPromptTemplate

from config import model
from graph.state import ResearchState
from prompts.synthesizer import HUMAN, SYNTHESIZER

synthesizer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYNTHESIZER),
        ("human", HUMAN),
    ]
)

chain = synthesizer_prompt | model


def synthesizer_node(state: ResearchState):
    draft = chain.invoke({
        "query": state["query"],
        "web_results": state.get("web_results", ""),
        "rag_results": state.get("rag_results", ""),
    })
    content = str(getattr(draft, "content", draft)).strip()
    return {"draft": content, "final_answer": content}

