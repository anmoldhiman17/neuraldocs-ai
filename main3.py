from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Embedding model
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector database
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings_model
)

# Retriever
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 6,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }
)

# LLM
llm = ChatMistralAI(
    model="mistral-small-2506"
)

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert AI tutor.

Answer the user's question using ONLY the provided context.

Rules:
- Give detailed and easy-to-understand explanations.
- Explain concepts clearly.
- Use examples whenever possible.
- Keep the answer beginner-friendly.
- Do not make up information outside the context.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
        ),
        (
            "human",
            """
Context:
{context}

Question:
{question}
"""
        )
    ]
)

print("✅ RAG system is ready to answer questions")
print("Press 0 to exit")

while True:

    query = input("\nYou : ")

    if query == "0":
        print("\n👋 Exiting RAG system...")
        break

    # Retrieve relevant documents
    docs = retriever.invoke(query)

    # Create context
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Build final prompt
    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": query
        }
    )

    # Generate response
    response = llm.invoke(final_prompt)

    # Print answer
    print(f"\n🤖 AI : {response.content}")