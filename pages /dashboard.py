"""
Dashboard Page — Welcome screen with stats and quick actions.
"""

import streamlit as st
from datetime import datetime


def render_dashboard():
    """Render the main dashboard page."""

    # ── Hero Section ─────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div style="margin-bottom:1rem;">
            <span class="badge badge-info">✨ AI-Powered Knowledge Engine</span>
        </div>
        <h1 class="hero-title">NeuralDocs AI</h1>
        <p class="hero-subtitle">
            Upload your documents, ask questions, and get instant AI-powered answers
            backed by your own knowledge base. Powered by RAG technology.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats Row ────────────────────────────────────────────
    num_docs = len(st.session_state.uploaded_documents)
    num_messages = len(st.session_state.chat_history)
    num_sessions = st.session_state.chat_sessions_count
    total_pages = sum(
        doc.get("pages", 0)
        for doc in st.session_state.uploaded_documents
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{num_docs}</div>
            <div class="stat-label">📄 Documents</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card" style="--gradient-1: linear-gradient(135deg, #06b6d4, #6366f1);">
            <div class="stat-number" style="background:linear-gradient(135deg,#06b6d4,#6366f1);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{total_pages}</div>
            <div class="stat-label">📑 Total Pages</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="background:linear-gradient(135deg,#8b5cf6,#ec4899);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{num_messages}</div>
            <div class="stat-label">💬 Messages</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="background:linear-gradient(135deg,#10b981,#06b6d4);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{num_sessions}</div>
            <div class="stat-label">🔄 Sessions</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Actions ────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>⚡ Quick Actions</h2>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2rem;">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">📚</div>
            <h3 style="color:var(--text-primary); font-size:1.1rem; margin-bottom:0.4rem;">
                Upload Documents
            </h3>
            <p style="color:var(--text-secondary); font-size:0.85rem; line-height:1.5;">
                Add PDF books and papers to your knowledge base
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📤 Upload Now", key="dash_upload", use_container_width=True):
            st.session_state.current_page = "Knowledge Base"
            st.rerun()

    with col_b:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2rem;">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">💬</div>
            <h3 style="color:var(--text-primary); font-size:1.1rem; margin-bottom:0.4rem;">
                Ask Questions
            </h3>
            <p style="color:var(--text-secondary); font-size:0.85rem; line-height:1.5;">
                Chat with your documents using AI-powered Q&A
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💬 Start Chat", key="dash_chat", use_container_width=True):
            st.session_state.current_page = "Chat"
            st.rerun()

    with col_c:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2rem;">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">⚙️</div>
            <h3 style="color:var(--text-primary); font-size:1.1rem; margin-bottom:0.4rem;">
                Configure
            </h3>
            <p style="color:var(--text-secondary); font-size:0.85rem; line-height:1.5;">
                Set up API keys, models, and retrieval settings
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚙️ Settings", key="dash_settings", use_container_width=True):
            st.session_state.current_page = "Settings"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── How It Works ─────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>🔬 How It Works</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:1.5rem; text-align:center;">
            <div>
                <div style="font-size:2rem; margin-bottom:0.5rem;">📄</div>
                <h4 style="color:var(--text-primary); font-size:0.9rem; margin-bottom:0.3rem;">1. Upload</h4>
                <p style="color:var(--text-muted); font-size:0.78rem;">
                    Upload your PDF documents
                </p>
            </div>
            <div>
                <div style="font-size:2rem; margin-bottom:0.5rem;">🔪</div>
                <h4 style="color:var(--text-primary); font-size:0.9rem; margin-bottom:0.3rem;">2. Chunk</h4>
                <p style="color:var(--text-muted); font-size:0.78rem;">
                    Documents are split into smart chunks
                </p>
            </div>
            <div>
                <div style="font-size:2rem; margin-bottom:0.5rem;">🧬</div>
                <h4 style="color:var(--text-primary); font-size:0.9rem; margin-bottom:0.3rem;">3. Embed</h4>
                <p style="color:var(--text-muted); font-size:0.78rem;">
                    Embeddings stored in ChromaDB
                </p>
            </div>
            <div>
                <div style="font-size:2rem; margin-bottom:0.5rem;">🤖</div>
                <h4 style="color:var(--text-primary); font-size:0.9rem; margin-bottom:0.3rem;">4. Answer</h4>
                <p style="color:var(--text-muted); font-size:0.78rem;">
                    AI generates precise answers
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recent Documents ─────────────────────────────────────
    if st.session_state.uploaded_documents:
        st.markdown("""
        <div class="section-header">
            <h2>📄 Recent Documents</h2>
        </div>
        """, unsafe_allow_html=True)

        recent_docs = st.session_state.uploaded_documents[-3:]
        for doc in reversed(recent_docs):
            st.markdown(f"""
            <div class="file-card">
                <div class="file-icon">📄</div>
                <div class="file-info">
                    <h4>{doc['name']}</h4>
                    <div class="file-meta">
                        {doc.get('size_str', 'N/A')} · {doc.get('pages', '?')} pages
                        · Uploaded {doc.get('upload_date', 'recently')}
                    </div>
                </div>
                <div style="margin-left:auto;">
                    <span class="badge badge-success">✓ Indexed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tech Stack Footer ────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:1.5rem;">
        <p style="color:var(--text-muted); font-size:0.8rem; margin-bottom:0.7rem;">
            POWERED BY
        </p>
        <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
            <span class="badge badge-info">🦜 LangChain</span>
            <span class="badge badge-info">🔮 ChromaDB</span>
            <span class="badge badge-info">🤗 HuggingFace</span>
            <span class="badge badge-info">🌀 Mistral AI</span>
            <span class="badge badge-info">🎈 Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
