import re
from pathlib import Path

import streamlit as st

from graph.graph import build_graph


@st.cache_resource
def get_research_app():
    return build_graph()


def build_initial_state(query: str):
    return {
        "query": query,
        "route": "BOTH",
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


def append_chat(role: str, content: str):
    history = st.session_state.setdefault("chat_history", [])
    history.append({"role": role, "content": content})
    if len(history) > 12:
        history[:] = history[-12:]


def get_history_pairs():
    history = st.session_state.get("chat_history", [])
    pairs = []
    i = 0
    while i < len(history):
        user_msg = history[i] if history[i]["role"] == "user" else None
        assistant_msg = None
        if user_msg and i + 1 < len(history) and history[i + 1]["role"] == "assistant":
            assistant_msg = history[i + 1]
            i += 2
        else:
            i += 1
        pairs.append((user_msg, assistant_msg))
    return pairs


def save_uploaded_documents(uploaded_files):
    upload_dir = Path(__file__).resolve().parent / "documents" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for uploaded_file in uploaded_files:
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", uploaded_file.name)
        target_path = upload_dir / safe_name
        with open(target_path, "wb") as file_handle:
            file_handle.write(uploaded_file.getvalue())
        saved_paths.append(str(target_path))

    return saved_paths


research_app = get_research_app()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = {}
if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

st.set_page_config(page_title="AI Research Assistant", page_icon="🔎")

st.title("🔎 AI Research Assistant")

with st.sidebar:
    st.header("Menu")
    mode = st.radio("Mode", ["Chat", "Research"])

    st.divider()
    st.subheader("Upload documents")
    uploaded_files = st.file_uploader(
        "PDF, TXT, MD",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        saved_paths = save_uploaded_documents(uploaded_files)
        st.session_state.uploaded_documents = saved_paths
        st.caption(f"{len(saved_paths)} file(s) uploaded")
    elif st.session_state.uploaded_documents:
        st.caption(f"{len(st.session_state.uploaded_documents)} uploaded file(s)")
    else:
        st.caption("No files uploaded yet")

    st.divider()
    st.subheader("Chat history")
    history_pairs = get_history_pairs()
    if not history_pairs:
        st.caption("No chat history yet")
    else:
        for user_msg, assistant_msg in reversed(history_pairs):
            if user_msg is None:
                continue
            preview = user_msg["content"].strip().replace("\n", " ")
            if len(preview) > 40:
                preview = preview[:40] + "..."
            with st.expander(preview):
                st.markdown(f"**You:** {user_msg['content']}")
                if assistant_msg:
                    st.markdown(f"**Assistant:** {assistant_msg['content']}")

        if st.button("Clear chat history"):
            st.session_state.chat_history = []
            st.rerun()

if mode == "Chat":
    st.subheader("Chat")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask me anything...")
    if user_input:
        append_chat("user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                state = build_initial_state(user_input)
                result = research_app.invoke(state)
                response = result.get("final_answer") or result.get("draft") or "No answer produced."
            st.markdown(response)

        append_chat("assistant", response)
        st.session_state.last_result = result

else:
    st.subheader("Research")

    question = st.text_area(
        "Research question",
        placeholder="Ask a question you want researched...",
        height=140,
    )
    submitted = st.button("Run research")

    if submitted:
        if not question.strip():
            st.warning("Please enter a research question.")
        else:
            with st.spinner("Gathering evidence and drafting the answer..."):
                state = build_initial_state(question.strip())
                result = research_app.invoke(state)
            st.session_state.last_result = result
            append_chat("user", question.strip())
            append_chat("assistant", result.get("final_answer") or result.get("draft") or "No answer produced.")

    result = st.session_state.last_result
    if result:
        final_answer = result.get("final_answer") or result.get("draft") or "No final answer was produced."
        st.markdown("### Answer")
        st.markdown(final_answer)

        tab1, tab2, tab3, tab4 = st.tabs(["Web results", "Local documents", "Review", "Workflow"])

        with tab1:
            st.write(result.get("web_results") or "No web results were returned.")

        with tab2:
            st.write(result.get("rag_results") or "No local document context was available.")
            if result.get("sources"):
                with st.expander("Imported sources"):
                    st.code("\n".join(result["sources"]))

        with tab3:
            st.write(result.get("review") or "No review feedback was generated.")

        with tab4:
            st.json({
                "route": result.get("route", "N/A"),
                "review_passed": result.get("review_passed", False),
                "revision_number": result.get("revision_number", 0),
                "max_revisions": result.get("max_revisions", 3),
            })
    else:
        st.info("No research run yet. Enter a question above and click Run research.")