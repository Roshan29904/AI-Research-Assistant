from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def pdf_loader(file_path: str):
    """Load PDF files and return a list of documents."""
    path = Path(file_path)

    if not path.exists():
        return []

    if path.is_dir():
        documents = []
        for pdf_file in sorted(path.glob("*.pdf")):
            documents.extend(PyPDFLoader(str(pdf_file)).load())
        return documents

    return PyPDFLoader(str(path)).load()
