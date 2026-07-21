from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import model
from graph.state import ResearchState
from prompts.synthesizer import SYNTHESIZER, HUMAN

synthesizer_prompt = ChatPromptTemplate.from_messages(
    [("system", SYNTHESIZER),
     ("human", HUMAN)
    ]
)

chain = synthesizer_prompt | model | StrOutputParser()



def synthesizer_node(state: ResearchState):
    
    draft =  chain.invoke({
        "query": state["query"],
        "web_results": state["web_results"],
        "rag_results": state["rag_results"]
    
    })
    return draft
