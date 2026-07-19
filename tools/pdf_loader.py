from langchain_community.document_loaders import PyPDFLoader


def pdf_loader(file_path: str):
    """Load a pdf file and return a list of doucuments"""
    pdf_file = PyPDFLoader(file_path)
    documents = pdf_file.load()
    return documents