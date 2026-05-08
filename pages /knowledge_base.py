"""
Knowledge Base Page — Upload, manage and process PDF documents.
"""

import streamlit as st
import os
import time
from pathlib import Path
from datetime import datetime


def format_file_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def process_uploaded_file(uploaded_file):
    from backend.database import add_document_to_vectorstore

    save_dir = Path("/tmp/uploaded_docs")
    save_dir.mkdir(exist_ok=True)
    file_path = save_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    doc_info = add_document_to_vectorstore(
        file_path=str(file_path),
        chunk_size=st.session_state.chunk_size,
        chunk_overlap=st.session_state.chunk_overlap,
        embedding_model_name=st.session_state.embedding_model,
    )

    metadata = {
        "name": uploaded_file.name,
        "path": str(file_path),
        "size_bytes": uploaded_file.size,
        "size_str": format_file_size(uploaded_file.size),
        "pages": doc_info.get("num_pages", 0),
        "chunks": doc_info.get("num_chunks", 0),
        "upload_date": datetime.now().strftime("%b %d, %Y %H:%M"),
        "status": "indexed",
    }
    return metadata


def render_knowledge_base():

    st.markdown("""
    <div class="section-header">
        <h2>📚 Knowledge Base</h2>
    </div>
    <p style="color:var(--text-secondary); margin-top:-0.8rem;
              margin-bottom:1.5rem; font-size:0.92rem;">
        Upload PDF documents to build your AI knowledge base.
        Documents are chunked, embedded, and stored for intelligent retrieval.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
            <span style="font-size:1.3rem;">📤</span>
            <h3 style="margin:0; color:var(--text-primary); font-size:1.1rem;">
                Upload Documents
            </h3>
        </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Drag and drop PDF files here",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader",
        help="Upload one or more PDF files to add to your knowledge base.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_files:
        existing_names = {doc["name"] for doc in st.session_state.uploaded_documents}
        new_files = [f for f in uploaded_files if f.name not in existing_names]

        if new_files:
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:1.5rem;">
                <p style="color:var(--text-primary); font-weight:600;">
                    🆕 {len(new_files)} new file(s) ready to process
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"🚀 Process {len(new_files)} Document(s)",
                key="process_btn",
                use_container_width=True,
            ):
                if not st.session_state.mistral_api_key:
                    st.error("⚠️ Please set your Mistral API key in Settings first.")
                    return

                os.environ["MISTRAL_API_KEY"] = st.session_state.mistral_api_key
                progress_bar = st.progress(0)
                status_text = st.empty()

                for idx, file in enumerate(new_files):
                    progress_bar.progress(idx / len(new_files))
                    status_text.markdown(f"""
                    <div style="display:flex; align-items:center; gap:0.5rem;
                                color:var(--text-secondary); font-size:0.9rem;">
                        <span>⏳</span>
                        Processing <strong style="color:var(--text-primary);">
                        {file.name}</strong> ({idx + 1}/{len(new_files)})
                    </div>
                    """, unsafe_allow_html=True)

                    try:
                        metadata = process_uploaded_file(file)
                        st.session_state.uploaded_documents.append(metadata)
                    except Exception as e:
                        st.error(f"❌ Error processing {file.name}: {str(e)}")
                        continue

                progress_bar.progress(1.0)
                status_text.empty()
                progress_bar.empty()
                st.toast("✅ All documents processed successfully!", icon="🎉")
                st.balloons()
                time.sleep(1)
                st.rerun()

        else:
            st.info("ℹ️ All selected files have already been processed.")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    documents = st.session_state.uploaded_documents

    st.markdown(f"""
    <div class="section-header">
        <h2>📄 Indexed Documents ({len(documents)})</h2>
    </div>
    """, unsafe_allow_html=True)

    if not documents:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:3rem;">
            <div style="font-size:3rem; margin-bottom:1rem; opacity:0.5;">📭</div>
            <h3 style="color:var(--text-secondary); font-weight:500;">No documents yet</h3>
            <p style="color:var(--text-muted); font-size:0.85rem;">
                Upload your first PDF to get started
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    search_query = st.text_input(
        "🔍 Search documents...",
        placeholder="Type to filter documents...",
        key="doc_search",
    )

    filtered_docs = documents
    if search_query:
        filtered_docs = [
            d for d in documents if search_query.lower() in d["name"].lower()
        ]

    for idx, doc in enumerate(reversed(filtered_docs)):
        col_info, col_action = st.columns([5, 1])

        with col_info:
            st.markdown(f"""
            <div class="file-card">
                <div class="file-icon">📄</div>
                <div class="file-info" style="flex:1;">
                    <h4>{doc['name']}</h4>
                    <div class="file-meta">
                        {doc.get('size_str', 'N/A')} ·
                        {doc.get('pages', '?')} pages ·
                        {doc.get('chunks', '?')} chunks ·
                        {doc.get('upload_date', '')}
                    </div>
                </div>
                <span class="badge badge-success">✓ Indexed</span>
            </div>
            """, unsafe_allow_html=True)

        with col_action:
            st.markdown("<div style='padding-top:0.8rem;'>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"del_{doc['name']}_{idx}", help="Delete document"):
                try:
                    file_path = doc.get("path", "")
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                    st.session_state.uploaded_documents = [
                        d for d in st.session_state.uploaded_documents
                        if d["name"] != doc["name"]
                    ]
                    st.toast(f"🗑️ Removed {doc['name']}", icon="✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

    total_pages = sum(d.get("pages", 0) for d in documents)
    total_chunks = sum(d.get("chunks", 0) for d in documents)

    st.markdown(f"""
    <div class="glass-card" style="margin-top:1.5rem;">
        <div style="display:flex; justify-content:space-around; text-align:center;">
            <div>
                <div style="font-size:1.5rem; font-weight:700; color:var(--accent-blue);">
                    {len(documents)}
                </div>
                <div style="color:var(--text-muted); font-size:0.8rem;">Documents</div>
            </div>
            <div>
                <div style="font-size:1.5rem; font-weight:700; color:var(--accent-purple);">
                    {total_pages}
                </div>
                <div style="color:var(--text-muted); font-size:0.8rem;">Pages</div>
            </div>
            <div>
                <div style="font-size:1.5rem; font-weight:700; color:var(--accent-cyan);">
                    {total_chunks}
                </div>
                <div style="color:var(--text-muted); font-size:0.8rem;">Chunks</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ CORRECTLY INDENTED — inside render_knowledge_base()
    # Mobile-friendly Go to Chat button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "💬 Start Chatting Now →",
            key="goto_chat_kb",
            use_container_width=True,
        ):
            st.session_state.current_page = "Chat"
            st.rerun()
