import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEmbeddings, HuggingFaceEndpoint

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def _resolve_path(value: str | None, default: Path) -> str:
    if value:
        return value
    return str(default)


HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen2.5-7B-Instruct")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_DB_PATH = _resolve_path(os.getenv("VECTOR_DB_PATH"), BASE_DIR / "vectorestore" / "faiss_index")
DOCUMENTS_PATH = _resolve_path(os.getenv("DOCUMENTS_PATH"), BASE_DIR / "documents")
CHECKPOINT_DB = _resolve_path(os.getenv("CHECKPOINT_DB"), BASE_DIR / "memory.db")

llm = HuggingFaceEndpoint(
    repo_id=MODEL_ID,
    task="text-generation",
    max_new_tokens=1024,
    temperature=0.4,
    huggingfacehub_api_token=HF_TOKEN,
)
model = ChatHuggingFace(llm=llm)
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

__all__ = [
    "model",
    "embeddings",
    "VECTOR_DB_PATH",
    "DOCUMENTS_PATH",
    "CHECKPOINT_DB",
]
