from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import DOCUMENTS_PATH, VECTOR_DB_PATH, embeddings

from tools.pdf_loader import pdf_loader

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)


def create_vectorstore():
    """load pdf splite them in chunks and create a vector store using FAISS"""
    documents = pdf_loader(DOCUMENTS_PATH)
    
    chunks = text_splitter.split_documents(documents)
    
    vector_store = FAISS.from_documents(
        embedding=embeddings,
        documents=chunks
    )
    Path(VECTOR_DB_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )
    vector_store.save_local(VECTOR_DB_PATH)
    
    return vector_store



def load_vector_store():
    """Load the faiss index and if it doesn't exist then create one"""
    index_file = Path(VECTOR_DB_PATH)/"index_faiss"
    
    if not index_file.exists():
        return create_vectorstore()
    
    load = FAISS.load_local(
        folder_path=VECTOR_DB_PATH,
        embeddings=embeddings
    )
    
    return load



def retriever(k: int=4):
    """Retures a retriever for semantic search"""
    vector_store = load_vector_store()
    retriev = vector_store.as_retriever(
        search_Kwargs={"K": k}
    )    
    return retriev

