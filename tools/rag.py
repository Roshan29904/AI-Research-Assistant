from langchain_core.documents import Document

from tools.vectorstore import get_retriever


def retrieve_documents(query: str) -> list[Document]:
    """Get relevant documents from the vector store."""
    retriever = get_retriever()
    if retriever is None:
        return []
    return retriever.invoke(query)


def build_context(documents: list[Document]) -> str:
    """Convert retrieved documents into a single context string."""
    if not documents:
        return "No local document context is available for this query."

    context = []
    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        context.append(f"Document {i}, Source: {source}, Page: {page}, content: {doc.page_content}")
    return "\n".join(context)


def extract_source(documents: list[Document]) -> list[str]:
    """Extract unique source files from retrived documents."""
    sources = []
    for doc in documents:
        source = doc.metadata.get("source")
        if source and source not in sources:
            sources.append(source)
    return sources


def search_documents(query: str):
    """Perform semantic search over the vector store."""
    documents = retrieve_documents(query)
    context = build_context(documents)
    sources = extract_source(documents)
    return context, sources

