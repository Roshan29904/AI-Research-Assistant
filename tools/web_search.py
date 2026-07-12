from langchain_community.tools import DuckDuckGoSearchResults


web_search_tool= DuckDuckGoSearchResults(output_format="list")

def web_search(query: str) -> list:
    """search the web and reslove the user's query. Return list of search results"""
    web_search_results = web_search_tool.invoke(query)
    return web_search_results

