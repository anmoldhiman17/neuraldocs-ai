<div align="center">

<br/>

```
███╗   ██╗███████╗██╗   ██╗██████╗  █████╗ ██╗     ██████╗  ██████╗  ██████╗███████╗
████╗  ██║██╔════╝██║   ██║██╔══██╗██╔══██╗██║     ██╔══██╗██╔═══██╗██╔════╝██╔════╝
██╔██╗ ██║█████╗  ██║   ██║██████╔╝███████║██║     ██║  ██║██║   ██║██║     ███████╗
██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██╔══██║██║     ██║  ██║██║   ██║██║     ╚════██║
██║ ╚████║███████╗╚██████╔╝██║  ██║██║  ██║███████╗██████╔╝╚██████╔╝╚██████╗███████║
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝  ╚═════╝╚══════╝
```

### 🧠 *Intelligent Document Q&A — Powered by RAG*

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-HuggingFace_Spaces-FF4B4B?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/spaces/Anmoldhiman17/neuraldocs-ai)
[![GitHub Repo](https://img.shields.io/badge/📦_Source_Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/anmoldhiman17/neuraldocs-ai)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **Upload any PDF. Ask anything. Get intelligent answers — grounded in your documents.**
>
> NeuralDocs AI is a full-stack Retrieval-Augmented Generation (RAG) application that transforms static documents into a living, queryable knowledge base powered by vector embeddings and large language models.

<br/>

---

</div>

<br/>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 Intelligent Retrieval
- **MMR (Maximal Marginal Relevance)** retrieval for diverse, non-redundant results
- **ChromaDB** vector store with persistent embeddings
- Configurable `top-k`, `fetch-k`, and `lambda` parameters
- Smart chunk-level source filtering

</td>
<td width="50%">

### 💬 ChatGPT-Style Interface
- Real-time streaming responses
- Full conversation history
- Source attribution per message
- Suggested starter questions

</td>
</tr>
<tr>
<td width="50%">

### 📄 Document Management
- Drag-and-drop multi-PDF upload
- Live processing progress with page/chunk stats
- Search & filter indexed documents
- One-click document deletion

</td>
<td width="50%">

### ⚙️ Full Customization
- Embedding model selection
- Adjustable chunk size & overlap
- Temperature control for LLM
- Vector DB reset & data management

</td>
</tr>
<tr>
<td width="50%">

### 📱 Mobile-Ready
- Sticky top navigation bar for mobile users
- Responsive layout across all screen sizes
- "Start Chatting Now →" shortcut after upload

</td>
<td width="50%">

### 🔐 Secure by Design
- API key loaded from environment secrets
- Never exposed in the UI when set via HF Secrets
- `/tmp`-based storage for HuggingFace Spaces compliance

</td>
</tr>
</table>

<br/>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      NeuralDocs AI                          │
│                    Streamlit Frontend                       │
├───────────────┬─────────────────────┬───────────────────────┤
│  Knowledge    │      Chat Page      │      Settings         │
│  Base Page    │  (RAG Interface)    │      Page             │
│  PDF Upload   │  Query + Answer     │  Config & Tuning      │
└──────┬────────┴──────────┬──────────┴───────────────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐    ┌──────────────────┐
│  PyPDFLoader│    │  RAG Pipeline    │
│  + Splitter │    │  ┌────────────┐  │
│             │    │  │  Retriever │  │
│  Chunk Size │    │  │  (MMR)     │  │
│  + Overlap  │    │  └────┬───────┘  │
└──────┬──────┘    │       │          │
       │           │  ┌────▼───────┐  │
       ▼           │  │  Mistral   │  │
┌─────────────┐    │  │  AI LLM    │  │
│  HuggingFace│    │  └────────────┘  │
│  Embeddings │    └──────────────────┘
│  all-MiniLM │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ChromaDB   │
│  Vector     │
│  Store      │
│  /tmp/      │
└─────────────┘
```

<br/>

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/anmoldhiman17/neuraldocs-ai.git
cd neuraldocs-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Mistral API key

```bash
# Linux / macOS
export MISTRAL_API_KEY="your_key_here"

# Windows (PowerShell)
$env:MISTRAL_API_KEY="your_key_here"
```

> Get your free API key at → [console.mistral.ai](https://console.mistral.ai/)

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

<br/>

---

## ☁️ Deploy on HuggingFace Spaces

[![Deploy to HuggingFace](https://img.shields.io/badge/Deploy_to-HuggingFace_Spaces-FF4B4B?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/new-space)

1. Create a new **Streamlit** Space on HuggingFace
2. Push this repo to the Space:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/neuraldocs-ai
   git push hf main
   ```
3. Go to **Settings → Repository Secrets** and add:
   ```
   MISTRAL_API_KEY = your_key_here
   ```
4. Wait for the Space to build — you're live! 🚀

> **Note:** HuggingFace Spaces uses a read-only filesystem. The app automatically uses `/tmp/` for all file writes (ChromaDB + uploaded PDFs). Data resets on Space restart — for persistent storage, connect a HuggingFace Dataset.

<br/>

---

## 📁 Project Structure

```
neuraldocs-ai/
│
├── app.py                     # 🚀 Main Streamlit entry point + navigation
│
├── pages/
│   ├── __init__.py
│   ├── dashboard.py           # 📊 Stats overview page
│   ├── knowledge_base.py      # 📚 PDF upload & management
│   ├── chat.py                # 💬 RAG chat interface
│   └── settings.py            # ⚙️  API keys, model & retrieval config
│
├── backend/
│   ├── __init__.py
│   ├── database.py            # 🗄️  ChromaDB vector store CRUD
│   ├── embeddings.py          # 🧬 HuggingFace embedding model loader
│   ├── retriever.py           # 🔍 MMR retriever setup
│   ├── rag_pipeline.py        # 🤖 Full RAG chain (retrieve → prompt → LLM)
│   └── utils.py               # 🛠️  Shared helpers & directory management
│
├── assets/
│   └── style.css              # 🎨 Custom dark glassmorphism theme
│
├── .streamlit/
│   └── config.toml            # ⚙️  Streamlit server config
│
├── Dockerfile                 # 🐳 HuggingFace Spaces Docker config
├── requirements.txt           # 📦 Python dependencies
└── README.md
```

<br/>

---

## 🧬 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | [Streamlit](https://streamlit.io) | UI framework — pages, chat, widgets |
| **LLM** | [Mistral AI](https://mistral.ai) (`mistral-small-2506`) | Answer generation |
| **Embeddings** | [HuggingFace](https://huggingface.co) (`all-MiniLM-L6-v2`) | Text vectorization |
| **Vector DB** | [ChromaDB](https://www.trychroma.com) | Persistent embedding storage |
| **RAG Framework** | [LangChain](https://langchain.com) | Document loading, splitting, retrieval |
| **PDF Parsing** | `PyPDFLoader` | Extract text from uploaded PDFs |
| **Retrieval Strategy** | MMR (Maximal Marginal Relevance) | Diverse, non-redundant chunk retrieval |
| **Deployment** | [HuggingFace Spaces](https://huggingface.co/spaces) | Cloud hosting (Docker) |

<br/>

---

## ⚙️ Configuration Reference

All parameters are tunable from the **Settings page** in the UI:

| Parameter | Default | Description |
|---|---|---|
| `embedding_model` | `all-MiniLM-L6-v2` | HuggingFace model for vectorizing text |
| `chunk_size` | `1000` | Characters per document chunk |
| `chunk_overlap` | `200` | Overlap between consecutive chunks |
| `retrieval_k` | `6` | Number of chunks returned per query |
| `retrieval_fetch_k` | `20` | Candidate pool size before MMR filtering |
| `retrieval_lambda` | `0.5` | MMR diversity/relevance tradeoff (0=diverse, 1=relevant) |
| `temperature` | `0.3` | LLM creativity (0=focused, 1=creative) |

<br/>

---

## 🗺️ Roadmap

- [ ] 🌐 Web URL ingestion (scrape & embed web pages)
- [ ] 🗂️ Multi-collection support (separate knowledge bases)
- [ ] 🔗 HuggingFace Datasets integration for persistent storage
- [ ] 📊 Document analytics & query history dashboard
- [ ] 🧑‍🤝‍🧑 Multi-user support with isolated sessions
- [ ] 📤 Export chat history as PDF/Markdown
- [ ] 🌍 Multilingual document support

<br/>

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repo and clone
git clone https://github.com/YOUR_USERNAME/neuraldocs-ai.git

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Commit your changes
git commit -m "feat: add your feature"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

<br/>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<br/>

---

<div align="center">

**Built with ❤️ by [Anmol Dhiman](https://github.com/anmoldhiman17)**

*Powered by LangChain · ChromaDB · Mistral AI · Streamlit*

<br/>

[![Star this repo](https://img.shields.io/github/stars/anmoldhiman17/neuraldocs-ai?style=social)](https://github.com/anmoldhiman17/neuraldocs-ai/stargazers)
[![Follow on GitHub](https://img.shields.io/github/followers/anmoldhiman17?style=social)](https://github.com/anmoldhiman17)

<br/>

> *"The best way to understand a document is to have a conversation with it."*

</div>
