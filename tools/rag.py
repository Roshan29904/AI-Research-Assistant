from langchain_core.documents import Document

from tools.vectorstore import get_retriever

retriever = get_retriever()

def retrieve_documents(query: str) -> list[Document]:
    """get relivent documents from the vector store"""
    return retriever.invoke(query)


def build_context(documents: list[Document]) -> str:
    """Converts retrieved documents into a single context string"""
    context = []
    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source")
        page = doc.metadata.get("page")
        context.append(f"Document {i}, Source: {source}, Page: {page}, content: {doc.page_content}")
    return "\n".join(context)
    
    

def extract_source(documents: list[Document]) -> list[str]:
    """Extract unique source files from retrived documents"""
    sources = []
    for doc in documents:
        source = doc.metadata.get("source")
        if source not in sources:
            sources.append(source)
    return sources
        

def search_documents(query: str):
    """perform semantic search over the vector store"""
    documents = retrieve_documents(query)
    context = build_context(documents)
    sources = extract_source(documents)
    return context, sources

