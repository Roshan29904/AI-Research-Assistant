from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import DOCUMENTS_PATH, VECTOR_DB_PATH, embeddings
from tools.pdf_loader import pdf_loader

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def create_vectorstore():
    """Load PDFs, split them into chunks, and create a FAISS vector store."""
    documents = pdf_loader(DOCUMENTS_PATH)
    if not documents:
        Path(VECTOR_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        return None

    chunks = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(embedding=embeddings, documents=chunks)
    Path(VECTOR_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(VECTOR_DB_PATH)
    return vector_store


def load_vector_store():
    """Load the FAISS index and create it if it does not exist."""
    index_path = Path(VECTOR_DB_PATH)
    if not index_path.exists() or not any(index_path.iterdir()):
        return create_vectorstore()

    try:
        return FAISS.load_local(folder_path=VECTOR_DB_PATH, embeddings=embeddings)
    except Exception:
        return create_vectorstore()


def get_retriever(k: int = 4):
    """Return a semantic retriever for the vector store."""
    vector_store = load_vector_store()
    if vector_store is None:
        return None
    return vector_store.as_retriever(search_kwargs={"k": k})

