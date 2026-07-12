import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings

load_dotenv()


HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

MODEL_ID = os.getenv("MODEL_ID")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")

DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")

CHECKPOINT_DB = os.getenv("CHECKPOINT_DB")



llm = HuggingFaceEndpoint(
    repo_id = MODEL_ID,
    task = "text=generation",
    max_new_tokens=1024,
    temperature=0.4,
    huggingfacehub_api_token=HF_TOKEN
    
)
model = ChatHuggingFace(llm = llm)



embeddings = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)


__all__ = [
    "model",
    "embeddings",
    "VECTOR_DB_PATH",
    "DOCUMENTS_PATH",
    "CHECKPOINT_DB"
]

