"""
Embedding utilities — Load and cache embedding models.
"""

import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource(show_spinner=False)
def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Load and cache a HuggingFace embedding model.
    Uses Streamlit's cache_resource to avoid reloading on every interaction.
    Args:
        model_name: HuggingFace model identifier.
    Returns:
        HuggingFaceEmbeddings instance.
    """
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
