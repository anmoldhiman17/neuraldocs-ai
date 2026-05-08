"""
Settings Page — Configure API keys, models, and retrieval parameters.
"""

import streamlit as st
import os
import shutil


def render_settings():
    """Render the Settings page."""

    st.markdown("""
    <div class="section-header">
        <h2>⚙️ Settings</h2>
    </div>
    <p style="color:var(--text-secondary); margin-top:-0.8rem; margin-bottom:1.5rem; font-size:0.92rem;">
        Configure your AI pipeline, API keys, and retrieval parameters.
    </p>
    """, unsafe_allow_html=True)

    # ── API Configuration ─────────────────────────────────────
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
            <span style="font-size:1.3rem;">🔑</span>
            <h3 style="margin:0; color:var(--text-primary); font-size:1.1rem;">API Configuration</h3>
        </div>
    """, unsafe_allow_html=True)

    # ✅ If API key already loaded from HF Secrets, show masked status only
    env_key = os.getenv("MISTRAL_API_KEY", "")

    if env_key:
        st.session_state.mistral_api_key = env_key
        st.markdown("""
        <div style="padding:1rem; background:rgba(16,185,129,0.08);
                    border:1px solid rgba(16,185,129,0.2);
                    border-radius:12px; display:flex; align-items:center; gap:0.7rem;">
            <span style="font-size:1.2rem;">✅</span>
            <div>
                <div style="color:#10b981; font-weight:600; font-size:0.9rem;">
                    API Key Loaded from Environment
                </div>
                <div style="color:var(--text-muted); font-size:0.78rem; margin-top:0.2rem;">
                    Securely configured via HuggingFace Secrets
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        api_key = st.text_input(
            "Mistral API Key",
            value=st.session_state.mistral_api_key,
            type="password",
            placeholder="Enter your Mistral API key...",
            help="Get your API key from https://console.mistral.ai/",
            key="settings_api_key",
        )
        if api_key != st.session_state.mistral_api_key:
            st.session_state.mistral_api_key = api_key
            os.environ["MISTRAL_API_KEY"] = api_key

        if api_key:
            st.markdown(
                '<span class="badge badge-success">✓ API Key Configured</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="badge badge-warning">⚠ API Key Required</span>',
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Two-column layout ─────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:1.5rem;">
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
                <span style="font-size:1.3rem;">🧬</span>
                <h3 style="margin:0; color:var(--text-primary); font-size:1.05rem;">
                    Embedding Model
                </h3>
            </div>
        """, unsafe_allow_html=True)

        embedding_options = [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2",
            "sentence-transformers/paraphrase-MiniLM-L6-v2",
        ]

        current_idx = 0
        if st.session_state.embedding_model in embedding_options:
            current_idx = embedding_options.index(st.session_state.embedding_model)

        selected_embedding = st.selectbox(
            "Model",
            embedding_options,
            index=current_idx,
            key="settings_embedding",
            help="Choose the embedding model for document vectorization.",
        )
        st.session_state.embedding_model = selected_embedding

        st.markdown("""
        <p style="color:var(--text-muted); font-size:0.78rem; margin-top:0.5rem;">
            💡 all-MiniLM-L6-v2 is recommended for balanced speed/quality.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:1.5rem;">
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
                <span style="font-size:1.3rem;">🤖</span>
                <h3 style="margin:0; color:var(--text-primary); font-size:1.05rem;">
                    LLM Configuration
                </h3>
            </div>
        """, unsafe_allow_html=True)

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.05,
            key="settings_temp",
            help="Lower = more focused; Higher = more creative.",
        )
        st.session_state.temperature = temperature

        st.markdown(f"""
        <p style="color:var(--text-muted); font-size:0.78rem; margin-top:0.5rem;">
            Current: {temperature} · {"Focused" if temperature < 0.3 else "Balanced" if temperature < 0.7 else "Creative"}
        </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Chunking Settings ─────────────────────────────────────
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
            <span style="font-size:1.3rem;">🔪</span>
            <h3 style="margin:0; color:var(--text-primary); font-size:1.05rem;">
                Text Chunking
            </h3>
        </div>
    """, unsafe_allow_html=True)

    col_cs, col_co = st.columns(2)

    with col_cs:
        chunk_size = st.slider(
            "Chunk Size (characters)",
            min_value=200,
            max_value=3000,
            value=st.session_state.chunk_size,
            step=100,
            key="settings_chunk_size",
        )
        st.session_state.chunk_size = chunk_size

    with col_co:
        chunk_overlap = st.slider(
            "Chunk Overlap (characters)",
            min_value=0,
            max_value=500,
            value=st.session_state.chunk_overlap,
            step=50,
            key="settings_chunk_overlap",
        )
        st.session_state.chunk_overlap = chunk_overlap

    st.markdown(f"""
    <p style="color:var(--text-muted); font-size:0.78rem; margin-top:0.5rem;">
        📏 Chunk size: {chunk_size} chars · Overlap: {chunk_overlap} chars ·
        Overlap ratio: {chunk_overlap/chunk_size*100:.0f}%
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Retrieval Settings ────────────────────────────────────
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
            <span style="font-size:1.3rem;">🔍</span>
            <h3 style="margin:0; color:var(--text-primary); font-size:1.05rem;">
                Retrieval Settings (MMR)
            </h3>
        </div>
    """, unsafe_allow_html=True)

    col_k, col_fk, col_lambda = st.columns(3)

    with col_k:
        retrieval_k = st.slider(
            "Top K Results",
            min_value=1,
            max_value=20,
            value=st.session_state.retrieval_k,
            key="settings_k",
        )
        st.session_state.retrieval_k = retrieval_k

    with col_fk:
        retrieval_fetch_k = st.slider(
            "Fetch K (candidates)",
            min_value=5,
            max_value=50,
            value=st.session_state.retrieval_fetch_k,
            key="settings_fetch_k",
        )
        st.session_state.retrieval_fetch_k = retrieval_fetch_k

    with col_lambda:
        retrieval_lambda = st.slider(
            "Lambda (diversity)",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.retrieval_lambda,
            step=0.05,
            key="settings_lambda",
        )
        st.session_state.retrieval_lambda = retrieval_lambda

    st.markdown(f"""
    <p style="color:var(--text-muted); font-size:0.78rem; margin-top:0.5rem;">
        🔎 Returns top {retrieval_k} from {retrieval_fetch_k} candidates ·
        Lambda: {retrieval_lambda} ({"Diverse" if retrieval_lambda < 0.4 else "Balanced" if retrieval_lambda < 0.7 else "Relevant"})
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Data Management ───────────────────────────────────────
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
            <span style="font-size:1.3rem;">🗄️</span>
            <h3 style="margin:0; color:var(--text-primary); font-size:1.05rem;">
                Data Management
            </h3>
        </div>
    """, unsafe_allow_html=True)

    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        if st.button("🗑️ Clear Chat History", key="clear_history", use_container_width=True):
            st.session_state.chat_history = []
            st.toast("Chat history cleared!", icon="🗑️")
            st.rerun()

    with col_d2:
        if st.button("📄 Reset Documents", key="reset_docs", use_container_width=True):
            st.session_state.uploaded_documents = []
            # ✅ Fixed path to /tmp
            if os.path.exists("/tmp/uploaded_docs"):
                shutil.rmtree("/tmp/uploaded_docs")
                os.makedirs("/tmp/uploaded_docs")
            st.toast("Documents reset!", icon="📄")
            st.rerun()

    with col_d3:
        if st.button("💣 Reset Vector DB", key="reset_db", use_container_width=True):
            # ✅ Fixed path to /tmp
            if os.path.exists("/tmp/chroma_db"):
                shutil.rmtree("/tmp/chroma_db")
                os.makedirs("/tmp/chroma_db")
            st.session_state.uploaded_documents = []
            st.session_state.chat_history = []
            st.toast("Vector database reset!", icon="💣")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Current Configuration Summary ─────────────────────────
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
            <span style="font-size:1.3rem;">📋</span>
            <h3 style="margin:0; color:var(--text-primary); font-size:1.05rem;">
                Current Configuration
            </h3>
        </div>
    """, unsafe_allow_html=True)

    config_data = {
        "API Key": "✅ Configured" if st.session_state.mistral_api_key else "❌ Missing",
        "Embedding Model": st.session_state.embedding_model.split("/")[-1],
        "LLM": "mistral-small-2506",
        "Temperature": st.session_state.temperature,
        "Chunk Size": f"{st.session_state.chunk_size} chars",
        "Chunk Overlap": f"{st.session_state.chunk_overlap} chars",
        "Top K": st.session_state.retrieval_k,
        "Fetch K": st.session_state.retrieval_fetch_k,
        "Lambda": st.session_state.retrieval_lambda,
        "Documents": len(st.session_state.uploaded_documents),
    }

    config_html = ""
    for key, val in config_data.items():
        config_html += f"""
        <div style="display:flex; justify-content:space-between;
                    padding:0.45rem 0; border-bottom:1px solid var(--border-glass);">
            <span style="color:var(--text-secondary); font-size:0.85rem;">{key}</span>
            <span style="color:var(--text-primary); font-size:0.85rem; font-weight:500;">{val}</span>
        </div>
        """

    st.markdown(config_html + "</div>", unsafe_allow_html=True)
