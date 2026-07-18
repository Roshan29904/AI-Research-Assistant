from langchain_community.tools import DuckDuckGoSearchResults


web_search_tool= DuckDuckGoSearchResults(output_format="list")

def web_search(query: str) -> list:
    """search the web and reslove the user's query. Return list of search results"""
    web_search_results = web_search_tool.invoke(query)
    return web_search_results


def format_search_results(results: list) -> str:
    """converts web_search results into a clean string for the llm"""
    if not results:
        return "no web results found"
    formatted = []
    for index, result in enumerate(results, start=1):
        title = result.get("title", "No Title")
        snippet = result.get("snippet", "No Snippet")
        link = result.get("link", "No Link")
        formatted.append(f"""
                         Result {index} 
                         Title:{title}
                         Snippet:{snippet}
                         URL:{link}
                    """)
        
    return "\n".join(formatted)