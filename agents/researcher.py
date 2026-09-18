from graph.state import ResearchState
from tools.rag import search_documents
from tools.web_search import format_search_results, web_search


def web_search_node(state: ResearchState):
    """Node for web search using DuckDuckGo search."""
    query = state["query"]
    results = web_search(query)
    formatted_results = format_search_results(results)
    return {"web_results": formatted_results}


def rag_research_node(state: ResearchState):
    query = state["query"]
    rag_context, sources = search_documents(query)
    return {"rag_results": rag_context, "sources": sources}


def both_research_node(state: ResearchState):
    query = state["query"]
    web_result = web_search(query)
    formatted_results = format_search_results(web_result)
    rag_context, sources = search_documents(query)
    return {
        "web_results": formatted_results,
        "rag_results": rag_context,
        "sources": sources,
    }


    
    
