"""
Retriever module — Configure and return the ChromaDB retriever.
"""

from backend.database import get_vectorstore


def get_retriever(
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    search_type: str = "mmr",
    k: int = 6,
    fetch_k: int = 20,
    lambda_mult: float = 0.5,
):
    """
    Create a retriever from the ChromaDB vector store.
    Uses MMR (Maximal Marginal Relevance) by default for balanced
    relevance and diversity.
    Args:
        embedding_model_name: HuggingFace model identifier.
        search_type: 'mmr' or 'similarity'.
        k: Number of results to return.
        fetch_k: Number of candidates to fetch before MMR.
        lambda_mult: Diversity vs relevance trade-off (0=diverse, 1=relevant).
    Returns:
        A LangChain retriever instance, or None if no vectorstore exists.
    """
    vectorstore = get_vectorstore(embedding_model_name)

    if vectorstore is None:
        return None

    return vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs={
            "k": k,
            "fetch_k": fetch_k,
            "lambda_mult": lambda_mult,
        },
    )
