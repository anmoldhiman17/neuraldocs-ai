"""
RAG Pipeline — Full Retrieval-Augmented Generation pipeline.
"""

import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from backend.retriever import get_retriever


SYSTEM_PROMPT = """
You are an expert AI tutor and knowledge assistant named NeuralDocs AI.
Answer the user's question using ONLY the provided context from their documents.
Rules:
- Give detailed, well-structured, and easy-to-understand explanations.
- Explain concepts clearly with proper formatting.
- Use bullet points, numbered lists, and headings when appropriate.
- Use examples whenever possible to illustrate concepts.
- Keep the answer beginner-friendly but comprehensive.
- Use markdown formatting for better readability.
- If multiple documents provide relevant info, synthesize them.
- Do NOT make up information outside the context.
- Do NOT hallucinate or add knowledge not present in the documents.
If the answer is NOT present in the context, respond:
"I could not find the answer in your uploaded documents. Try uploading more relevant documents or rephrasing your question."
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    (
        "human",
        """
Context from documents:
{context}
---
User's Question:
{question}
Please provide a detailed, well-formatted answer:
"""
    ),
])


def get_rag_response(
    query: str,
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    retrieval_k: int = 6,
    retrieval_fetch_k: int = 20,
    retrieval_lambda: float = 0.5,
    temperature: float = 0.3,
    active_documents: list = None,  # ✅ NEW: only search these docs
) -> dict:

    retriever = get_retriever(
        embedding_model_name=embedding_model_name,
        k=retrieval_k,
        fetch_k=retrieval_fetch_k,
        lambda_mult=retrieval_lambda,
    )

    if retriever is None:
        raise ValueError("No vector database found. Please upload documents first.")

    retrieved_docs = retriever.invoke(query)

    if not retrieved_docs:
        return {
            "answer": "I could not find any relevant information in your documents.",
            "sources": [],
        }

    # ✅ Filter: only keep chunks from currently active documents
    if active_documents:
        active_names = set(active_documents)
        retrieved_docs = [
            doc for doc in retrieved_docs
            if doc.metadata.get("source_file", "") in active_names
        ]

    if not retrieved_docs:
        return {
            "answer": "I could not find relevant information in your currently uploaded documents. The results may be from previously deleted documents. Try re-uploading your documents.",
            "sources": [],
        }

    context = "\n\n---\n\n".join(doc.page_content for doc in retrieved_docs)

    sources = list(set(
        doc.metadata.get("source_file", doc.metadata.get("source", "Unknown"))
        for doc in retrieved_docs
    ))

    final_prompt = prompt_template.invoke({
        "context": context,
        "question": query,
    })

    llm = ChatMistralAI(
        model="mistral-small-2506",
        temperature=temperature,
        api_key=os.environ.get("MISTRAL_API_KEY"),
    )

    response = llm.invoke(final_prompt)

    return {
        "answer": response.content,
        "sources": sources,
    }
