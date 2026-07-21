from graph.state import ResearchState

def review_router(state: ResearchState):
    if state["review_passed"]:
        return "final"
    
    if state["revision_number"] >= state["max_revisions"]:
        return "final"
    
    return "research_again"

