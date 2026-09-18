import streamlit as st

from graph.graph import build_graph


@st.cache_resource
def get_research_app():
    return build_graph()


st.set_page_config(page_title="AI Research Assistant", page_icon="🔎", layout="wide")


def build_initial_state(query: str):
    return {
        "query": query,
        "route": "",
        "web_results": "",
        "rag_results": "",
        "draft": "",
        "final_answer": "",
        "review": "",
        "review_passed": False,
        "revision_number": 0,
        "max_revisions": 3,
        "sources": [],
        "messages": [],
    }


research_app = get_research_app()

st.title("AI Research Assistant")
st.caption("Search the web and local knowledge base to create a research brief.")

with st.form("research_form"):
    question = st.text_area(
        "Research question",
        placeholder="Ask a question you want researched...",
        height=120,
    )
    submitted = st.form_submit_button("Research")

if submitted:
    if not question.strip():
        st.warning("Please enter a research question.")
    else:
        with st.spinner("Researching and synthesizing the answer..."):
            state = build_initial_state(question.strip())
            result = research_app.invoke(state)
        st.session_state["last_result"] = result

if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    st.subheader("Final answer")
    final_answer = result.get("final_answer") or result.get("draft") or "No final answer was produced."
    st.markdown(final_answer)

    tabs = st.tabs(["Web results", "Local documents", "Review"])

    with tabs[0]:
        st.write(result.get("web_results") or "No web results were returned.")

    with tabs[1]:
        rag_results = result.get("rag_results") or "No local document context was available."
        st.write(rag_results)
        if result.get("sources"):
            st.code("\n".join(result["sources"]))

    with tabs[2]:
        st.write(result.get("review") or "No review feedback was generated.")
