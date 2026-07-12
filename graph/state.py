from typing import TypedDict, Annotated

def merge_list(old_list: list, new_list: list) -> list:
   if new_list is None:
       return old_list
   return old_list + new_list



class ResearchState(TypedDict):
    query: str
    route: str
    web_results: str
    rag_results: str
    draft: str
    final_answer: str
    review: str
    review_passed: bool
    revision_number: int
    max_revisions: int
    sources: Annotated[list[str],  merge_list]
    messages: Annotated[list[dict],  merge_list]
    