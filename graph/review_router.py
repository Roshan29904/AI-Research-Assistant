from graph.state import ResearchState


def review_router(state: ResearchState):
    if state.get("review_passed", False):
        return "final"

    revision_number = int(state.get("revision_number", 0))
    max_revisions = int(state.get("max_revisions", 3))

    if revision_number >= max_revisions:
        return "final"

    return "research_again"

