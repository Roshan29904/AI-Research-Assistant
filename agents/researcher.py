from graph.state import ResearchState
from tools.web_search import web_search, format_search_results
from tools.rag import search_documents


def web_search_node(state: ResearchState):
    """Node for web search using DuckDuckGo search"""
    query = state["query"]
    results = web_search(query)
    format_search_result = format_search_results(results)
    
    return format_search_result



def rag_research_node(state: ResearchState):
    query = state["query"]
    result = search_documents(query)
    return result


def both_research_node(state: ResearchState):
    query = state["query"]
    web_result = web_search(query)
    format_search_result = format_search_results(web_result)
    rag_result = search_documents(query)
    return format_search_result, rag_result


    
    

