from typing import Annotated, TypedDict


def merge_list(old_list: list | None, new_list: list | None) -> list:
    if new_list is None:
        return old_list or []
    if old_list is None:
        old_list = []
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
    sources: Annotated[list[str], merge_list]
    messages: Annotated[list[dict], merge_list]
