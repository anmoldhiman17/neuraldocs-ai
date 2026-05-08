"""
Chat Page — ChatGPT-style conversational interface for document Q&A.
"""

import streamlit as st
import os


def render_chat():
    """Render the Chat page."""

    # ── Header ───────────────────────────────────────────────
    col_title, col_actions = st.columns([4, 1])

    with col_title:
        st.markdown("""
        <div class="section-header">
            <h2>💬 AI Chat</h2>
            <span class="badge badge-info" style="margin-left:0.5rem;">RAG Powered</span>
        </div>
        <p style="color:var(--text-secondary); margin-top:-0.8rem; margin-bottom:1rem; font-size:0.9rem;">
            Ask questions about your uploaded documents. AI answers using your knowledge base.
        </p>
        """, unsafe_allow_html=True)

    with col_actions:
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.chat_sessions_count += 1
            st.rerun()

    # ── Pre-flight Checks ────────────────────────────────────
    if not st.session_state.mistral_api_key:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2.5rem;
                    border-color:rgba(245,158,11,0.3);">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">🔑</div>
            <h3 style="color:var(--text-primary); font-weight:600;">API Key Required</h3>
            <p style="color:var(--text-secondary); font-size:0.9rem;">
                Please configure your Mistral API key in the Settings page.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚙️ Go to Settings", key="goto_settings"):
            st.session_state.current_page = "Settings"
            st.rerun()
        return

    if not st.session_state.uploaded_documents:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2.5rem;
                    border-color:rgba(99,102,241,0.3);">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">📚</div>
            <h3 style="color:var(--text-primary); font-weight:600;">No Documents Uploaded</h3>
            <p style="color:var(--text-secondary); font-size:0.9rem;">
                Upload at least one PDF document to start chatting.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📤 Upload Documents", key="goto_kb"):
            st.session_state.current_page = "Knowledge Base"
            st.rerun()
        return

    # ── Chat Container ───────────────────────────────────────
    chat_container = st.container()

    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem;">
                <div style="font-size:3rem; margin-bottom:1rem;">🧠</div>
                <h3 style="color:var(--text-primary); font-weight:600; margin-bottom:0.5rem;">
                    Ready to Answer Your Questions
                </h3>
                <p style="color:var(--text-secondary); font-size:0.9rem; max-width:500px; margin:0 auto;">
                    Ask anything about your uploaded documents.
                    I'll find the most relevant information and provide detailed answers.
                </p>
                <div style="display:flex; gap:0.5rem; justify-content:center;
                            flex-wrap:wrap; margin-top:1.5rem;">
                    <span class="source-chip">📄 {num_docs} document(s) loaded</span>
                    <span class="source-chip">🔍 MMR retrieval active</span>
                    <span class="source-chip">🤖 Mistral AI</span>
                </div>
            </div>
            """.format(
                num_docs=len(st.session_state.uploaded_documents)
            ), unsafe_allow_html=True)

            st.markdown("""
            <p style="text-align:center; color:var(--text-muted); font-size:0.82rem;
                       margin-top:1.5rem; margin-bottom:0.7rem;">
                💡 Try asking:
            </p>
            """, unsafe_allow_html=True)

            suggestions = [
                "What is this document about?",
                "Summarize the key concepts",
                "Explain the main topics covered",
            ]
            cols = st.columns(3)
            for i, suggestion in enumerate(suggestions):
                with cols[i]:
                    if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                        st.session_state.pending_query = suggestion
                        st.rerun()

        else:
            # Render chat history
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; margin-bottom:1rem;">
                        <div class="chat-msg-user">{msg['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display:flex; align-items:flex-start; gap:0.7rem; margin-bottom:1rem;">
                        <div style="min-width:36px; height:36px; background:var(--gradient-1);
                                    border-radius:10px; display:flex; align-items:center;
                                    justify-content:center; font-size:1.1rem; margin-top:0.2rem;">
                            🧠
                        </div>
                        <div style="flex:1;">
                            <div class="chat-msg-ai">{msg['content']}</div>
                    """, unsafe_allow_html=True)

                    # ✅ Only show sources that are in currently uploaded documents
                    if msg.get("sources"):
                        active_doc_names = {
                            doc["name"] for doc in st.session_state.uploaded_documents
                        }
                        # Filter sources to only show currently active documents
                        filtered_sources = [
                            s for s in msg["sources"]
                            if s in active_doc_names
                        ]
                        if filtered_sources:
                            sources_html = "".join(
                                f'<span class="source-chip">📄 {s}</span>'
                                for s in filtered_sources[:5]
                            )
                            st.markdown(f"""
                                <div style="margin-top:0.3rem;">
                                    <span style="color:var(--text-muted); font-size:0.75rem;">
                                        Sources:
                                    </span>
                                    {sources_html}
                                </div>
                            """, unsafe_allow_html=True)

                    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Chat Input ───────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    pending = st.session_state.pop("pending_query", None)

    query = st.chat_input(
        "Ask a question about your documents...",
        key="chat_input",
    )

    if pending and not query:
        query = pending

    if query:
        os.environ["MISTRAL_API_KEY"] = st.session_state.mistral_api_key

        st.session_state.chat_history.append({
            "role": "user",
            "content": query,
        })

        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; margin-bottom:1rem;">
            <div class="chat-msg-user">{query}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner(""):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
            <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:1rem;">
                <div style="min-width:36px; height:36px; background:var(--gradient-1);
                            border-radius:10px; display:flex; align-items:center;
                            justify-content:center; font-size:1.1rem;">
                    🧠
                </div>
                <div class="chat-msg-ai shimmer" style="padding:1rem 1.5rem;">
                    <div style="display:flex; gap:0.3rem; align-items:center;">
                        <span style="animation: pulse 0.6s infinite;">●</span>
                        <span style="animation: pulse 0.6s infinite 0.2s;">●</span>
                        <span style="animation: pulse 0.6s infinite 0.4s;">●</span>
                        <span style="color:var(--text-muted); font-size:0.85rem; margin-left:0.5rem;">
                            Searching knowledge base...
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            try:
                from backend.rag_pipeline import get_rag_response

                # ✅ Pass only currently active document names for filtering
                active_documents = [
                    doc["name"] for doc in st.session_state.uploaded_documents
                ]

                result = get_rag_response(
                    query=query,
                    embedding_model_name=st.session_state.embedding_model,
                    retrieval_k=st.session_state.retrieval_k,
                    retrieval_fetch_k=st.session_state.retrieval_fetch_k,
                    retrieval_lambda=st.session_state.retrieval_lambda,
                    temperature=st.session_state.temperature,
                    active_documents=active_documents,  # ✅ KEY FIX
                )

                answer = result["answer"]
                sources = result.get("sources", [])

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

                typing_placeholder.empty()

            except Exception as e:
                typing_placeholder.empty()
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": [],
                })

        st.rerun()

    # ── Chat Info Footer ─────────────────────────────────────
    if st.session_state.chat_history:
        st.markdown(f"""
        <div style="text-align:center; margin-top:1rem;">
            <p style="color:var(--text-muted); font-size:0.75rem;">
                {len(st.session_state.chat_history)} messages ·
                {len(st.session_state.uploaded_documents)} documents indexed ·
                Powered by Mistral AI + RAG
            </p>
        </div>
        """, unsafe_allow_html=True)
