"""
╔══════════════════════════════════════════════════════════════╗
║                   NeuralDocs AI v2.0                        ║
║         Intelligent Document Q&A — RAG Application          ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

Path("/tmp/uploaded_docs").mkdir(exist_ok=True)
Path("/tmp/chroma_db").mkdir(exist_ok=True)
Path("assets").mkdir(exist_ok=True)

st.set_page_config(
    page_title="NeuralDocs AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    css_path = Path("assets/style.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: rgba(255,255,255,0.03);
            --bg-glass: rgba(255,255,255,0.05);
            --border-glass: rgba(255,255,255,0.08);
            --accent-blue: #6366f1;
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-pink: #ec4899;
            --accent-green: #10b981;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --gradient-1: linear-gradient(135deg, #6366f1, #8b5cf6);
            --gradient-2: linear-gradient(135deg, #06b6d4, #6366f1);
            --gradient-3: linear-gradient(135deg, #8b5cf6, #ec4899);
            --shadow-glow: 0 0 30px rgba(99,102,241,0.15);
            --radius: 16px;
            --radius-sm: 10px;
            --radius-lg: 24px;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        [data-testid="stSidebar"] {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border-glass) !important;
        }
        [data-testid="stHeader"] {
            background: transparent !important;
        }
        /* ── Hide default Streamlit elements ── */
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        /* ✅ Hide Streamlit default multi-page nav links completely */
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebarNav"] {display: none !important;}
        div[data-testid="stSidebarNavItems"] {display: none !important;}
        ul[data-testid="stSidebarNavItems"] {display: none !important;}
        [data-testid="stSidebarNavLink"] {display: none !important;}
        /* ── Glassmorphism Card ── */
        .glass-card {
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius);
            padding: 1.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.5s ease forwards;
        }
        .glass-card:hover {
            border-color: rgba(99,102,241,0.3);
            box-shadow: var(--shadow-glow);
            transform: translateY(-2px);
        }
        /* ── Stat Cards ── */
        .stat-card {
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius);
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: var(--gradient-1);
        }
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-glow);
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        /* ── Gradient Buttons ── */
        .gradient-btn {
            background: var(--gradient-1);
            color: white !important;
            border: none;
            border-radius: var(--radius-sm);
            padding: 0.7rem 1.8rem;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
        }
        .gradient-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99,102,241,0.4);
        }
        /* ── Hero Section ── */
        .hero-section {
            text-align: center;
            padding: 3rem 1rem;
            position: relative;
        }
        .hero-title {
            font-size: 3.2rem;
            font-weight: 900;
            background: linear-gradient(135deg, #f1f5f9, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        .hero-subtitle {
            color: var(--text-secondary);
            font-size: 1.15rem;
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }
        /* ── Badges ── */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-success {
            background: rgba(16,185,129,0.15);
            color: #10b981;
            border: 1px solid rgba(16,185,129,0.2);
        }
        .badge-info {
            background: rgba(99,102,241,0.15);
            color: #818cf8;
            border: 1px solid rgba(99,102,241,0.2);
        }
        .badge-warning {
            background: rgba(245,158,11,0.15);
            color: #f59e0b;
            border: 1px solid rgba(245,158,11,0.2);
        }
        /* ── Chat Bubbles ── */
        .chat-msg-user {
            background: var(--gradient-1);
            color: white;
            padding: 1rem 1.3rem;
            border-radius: 18px 18px 4px 18px;
            max-width: 80%;
            margin-left: auto;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            line-height: 1.6;
            animation: fadeInRight 0.3s ease;
        }
        .chat-msg-ai {
            background: var(--bg-glass);
            border: 1px solid var(--border-glass);
            color: var(--text-primary);
            padding: 1.2rem 1.5rem;
            border-radius: 18px 18px 18px 4px;
            max-width: 85%;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            line-height: 1.7;
            animation: fadeInLeft 0.3s ease;
        }
        /* ── File Cards ── */
        .file-card {
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius);
            padding: 1.2rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.3s ease;
            margin-bottom: 0.8rem;
            animation: fadeInUp 0.4s ease forwards;
        }
        .file-card:hover {
            border-color: rgba(99,102,241,0.3);
            box-shadow: var(--shadow-glow);
        }
        .file-icon {
            font-size: 2rem;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(99,102,241,0.1);
            border-radius: 12px;
        }
        .file-info h4 {
            margin: 0;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        .file-meta {
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 0.2rem;
        }
        /* ── Section Headers ── */
        .section-header {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 1.5rem;
        }
        .section-header h2 {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
        }
        .section-divider {
            height: 1px;
            background: var(--border-glass);
            margin: 2rem 0;
        }
        /* ── Sidebar Styling ── */
        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.5rem 0;
            margin-bottom: 1.5rem;
        }
        .sidebar-brand-icon { font-size: 1.8rem; }
        .sidebar-brand-text {
            font-size: 1.2rem;
            font-weight: 800;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .sidebar-brand-tag {
            font-size: 0.65rem;
            color: var(--text-muted);
            font-weight: 500;
        }
        /* ── Source Chip ── */
        .source-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.25rem 0.7rem;
            background: rgba(99,102,241,0.1);
            border: 1px solid rgba(99,102,241,0.2);
            border-radius: 999px;
            font-size: 0.72rem;
            color: #818cf8;
            font-weight: 500;
            margin: 0.15rem;
        }
        /* ── Animations ── */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInRight {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes fadeInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .shimmer {
            background: linear-gradient(90deg,
                rgba(255,255,255,0.03) 25%,
                rgba(255,255,255,0.08) 50%,
                rgba(255,255,255,0.03) 75%
            );
            background-size: 200% 100%;
            animation: shimmer 1.5s ease infinite;
        }
        /* ── Mobile Navigation ── */
        @media (max-width: 768px) {
            .hero-title { font-size: 2rem !important; }
            .stButton > button {
                font-size: 0.72rem !important;
                padding: 0.4rem 0.3rem !important;
            }
        }
        /* ── Streamlit Overrides ── */
        .stTextInput > div > div > input {
            background: var(--bg-glass) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius-sm) !important;
            color: var(--text-primary) !important;
            padding: 0.7rem 1rem !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
        }
        .stSelectbox > div > div {
            background: var(--bg-glass) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius-sm) !important;
        }
        div[data-testid="stFileUploader"] { background: transparent !important; }
        div[data-testid="stFileUploader"] > div {
            border: 2px dashed rgba(99,102,241,0.3) !important;
            border-radius: var(--radius) !important;
            background: rgba(99,102,241,0.02) !important;
        }
        .stButton > button {
            background: var(--gradient-1) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.55rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(99,102,241,0.35) !important;
        }
        .stSlider > div > div > div > div {
            background: var(--gradient-1) !important;
        }
        div[data-testid="stExpander"] {
            background: var(--bg-glass) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius) !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-glass);
            border-radius: var(--radius);
            padding: 0.3rem;
            gap: 0.3rem;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-sm);
            color: var(--text-secondary);
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background: var(--gradient-1) !important;
            color: white !important;
        }
        .stMarkdown a { color: var(--accent-blue) !important; }
        .stSpinner > div { border-top-color: var(--accent-blue) !important; }
        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.1);
            border-radius: 999px;
        }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
        /* ── Toast ── */
        div[data-testid="stToast"] {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius) !important;
        }
    </style>
    """, unsafe_allow_html=True)


load_css()


# ── Initialize session state ──────────────────────────────────
def init_session_state():
    defaults = {
        "current_page": "Dashboard",
        "uploaded_documents": [],
        "processing": False,
        "chat_history": [],
        "chat_sessions_count": 0,
        "mistral_api_key": os.getenv("MISTRAL_API_KEY", ""),
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "temperature": 0.3,
        "retrieval_k": 6,
        "retrieval_fetch_k": 20,
        "retrieval_lambda": 0.5,
        "theme": "dark",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


# ── Mobile Top Navigation ─────────────────────────────────────
def render_mobile_nav():
    """4-button top nav — works on both mobile and desktop."""
    pages = {
        "Dashboard": "📊",
        "Knowledge Base": "📚",
        "Chat": "💬",
        "Settings": "⚙️",
    }
    cols = st.columns(4)
    for i, (page_name, icon) in enumerate(pages.items()):
        with cols[i]:
            if st.button(
                f"{icon} {page_name}",
                key=f"topnav_{page_name}",
                use_container_width=True,
            ):
                st.session_state.current_page = page_name
                st.rerun()

    st.markdown(
        "<hr style='border:none; border-top:1px solid rgba(255,255,255,0.08);"
        " margin:0.5rem 0 1.5rem 0;'>",
        unsafe_allow_html=True,
    )


render_mobile_nav()


# ── Sidebar ───────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <span class="sidebar-brand-icon">🧠</span>
            <div>
                <div class="sidebar-brand-text">NeuralDocs AI</div>
                <div class="sidebar-brand-tag">Intelligent Document Q&A</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.markdown(
            "<p style='color:var(--text-muted); font-size:0.75rem;"
            "text-transform:uppercase; letter-spacing:0.1em; font-weight:600;"
            "margin-bottom:0.5rem;'>Navigation</p>",
            unsafe_allow_html=True,
        )

        pages = {
            "Dashboard": "📊",
            "Knowledge Base": "📚",
            "Chat": "💬",
            "Settings": "⚙️",
        }

        for page_name, icon in pages.items():
            if st.button(
                f"{icon}  {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
            ):
                st.session_state.current_page = page_name
                st.rerun()

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.markdown(
            "<p style='color:var(--text-muted); font-size:0.75rem;"
            "text-transform:uppercase; letter-spacing:0.1em; font-weight:600;"
            "margin-bottom:0.5rem;'>Quick Stats</p>",
            unsafe_allow_html=True,
        )

        num_docs = len(st.session_state.uploaded_documents)
        num_chats = len(st.session_state.chat_history)

        st.markdown(f"""
        <div style="display:flex; flex-direction:column; gap:0.5rem;">
            <div style="display:flex; justify-content:space-between;
                        padding:0.5rem 0.7rem; background:var(--bg-glass);
                        border-radius:8px; border:1px solid var(--border-glass);">
                <span style="color:var(--text-secondary); font-size:0.82rem;">
                    📄 Documents
                </span>
                <span style="color:var(--accent-blue); font-weight:700;">{num_docs}</span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        padding:0.5rem 0.7rem; background:var(--bg-glass);
                        border-radius:8px; border:1px solid var(--border-glass);">
                <span style="color:var(--text-secondary); font-size:0.82rem;">
                    💬 Messages
                </span>
                <span style="color:var(--accent-purple); font-weight:700;">{num_chats}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        api_key = st.session_state.get("mistral_api_key", "")
        if api_key:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:0.5rem;">
                <span style="width:8px;height:8px;border-radius:50%;
                             background:#10b981;display:inline-block;"></span>
                <span style="color:var(--text-secondary);font-size:0.8rem;">
                    API Connected
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:0.5rem;">
                <span style="width:8px;height:8px;border-radius:50%;
                             background:#ef4444;display:inline-block;"></span>
                <span style="color:var(--text-secondary);font-size:0.8rem;">
                    API Key Missing
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            "<div style='position:absolute; bottom:1rem; left:1rem; right:1rem;"
            "text-align:center;'>"
            "<p style='color:var(--text-muted); font-size:0.7rem;'>"
            "NeuralDocs AI v2.0<br>Built with ❤️ & LangChain</p></div>",
            unsafe_allow_html=True,
        )


render_sidebar()


# ── Page Router ───────────────────────────────────────────────
page = st.session_state.current_page

if page == "Dashboard":
    from pages.dashboard import render_dashboard
    render_dashboard()
elif page == "Knowledge Base":
    from pages.knowledge_base import render_knowledge_base
    render_knowledge_base()
elif page == "Chat":
    from pages.chat import render_chat
    render_chat()
elif page == "Settings":
    from pages.settings import render_settings
    render_settings()
