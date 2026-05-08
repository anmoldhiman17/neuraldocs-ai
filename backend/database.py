"""
Database module — ChromaDB vector store creation and management.
"""

import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from backend.embeddings import get_embedding_model

# ✅ Use /tmp for HuggingFace Spaces writable storage
CHROMA_DIR = "/tmp/chroma_db"


def add_document_to_vectorstore(
    file_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> dict:

    Path(CHROMA_DIR).mkdir(exist_ok=True)

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    num_pages = len(documents)

    file_name = os.path.basename(file_path)
    for doc in documents:
        doc.metadata["source_file"] = file_name

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    num_chunks = len(chunks)

    embeddings = get_embedding_model(embedding_model_name)

    chroma_sqlite = os.path.join(CHROMA_DIR, "chroma.sqlite3")
    if os.path.exists(chroma_sqlite):
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings,
        )
        vectorstore.add_documents(chunks)
    else:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR,
        )

    return {
        "num_pages": num_pages,
        "num_chunks": num_chunks,
        "file_name": file_name,
    }


def get_vectorstore(
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
):
    if not os.path.exists(CHROMA_DIR):
        return None

    embeddings = get_embedding_model(embedding_model_name)

    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )
