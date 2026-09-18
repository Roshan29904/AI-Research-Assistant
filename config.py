import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEmbeddings, HuggingFacePipeline
from transformers import pipeline

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def _resolve_path(value: str | None, default: Path) -> str:
    if value:
        return value
    return str(default)


HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
raw_model_id = (os.getenv("MODEL_ID") or "").strip().strip('"')
MODEL_ID = raw_model_id if raw_model_id and "Qwen/Qwen2.5-7B-Instruct" not in raw_model_id else "microsoft/Phi-3.5-mini-instruct"
INFERENCE_PROVIDER = (os.getenv("INFERENCE_PROVIDER") or "").strip() or None

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_DB_PATH = _resolve_path(os.getenv("VECTOR_DB_PATH"), BASE_DIR / "vectorestore" / "faiss_index")
DOCUMENTS_PATH = _resolve_path(os.getenv("DOCUMENTS_PATH"), BASE_DIR / "documents")
CHECKPOINT_DB = _resolve_path(os.getenv("CHECKPOINT_DB"), BASE_DIR / "memory.db")

text_pipeline = pipeline(
    "text-generation",
    model=MODEL_ID,
    tokenizer=MODEL_ID,
    token=HF_TOKEN,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.3,
    device_map="auto",
)
llm = HuggingFacePipeline(pipeline=text_pipeline)
model = ChatHuggingFace(llm=llm)
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

__all__ = [
    "model",
    "embeddings",
    "VECTOR_DB_PATH",
    "DOCUMENTS_PATH",
    "CHECKPOINT_DB",
]