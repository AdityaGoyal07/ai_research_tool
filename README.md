# AI Research Tool

A dual-mode Streamlit application that turns any set of news-article URLs into a fully searchable knowledge base in seconds.

* **Basic Mode (`main.py`)** – lightning-fast proof-of-concept.
* **Enhanced Mode (`enhanced_main.py`)** – feature-rich UI with automatic question suggestions, dark theme, and extra productivity tools.

| App | Entry-point | Audience | Key idea |
|-----|-------------|----------|----------|
| **Core** | `main.py` | Minimal, lightning-fast demo | Paste URLs → vector index → ask questions |
| **Enhanced** | `enhanced_main.py` | Power users & portfolio showcase | Same engine + smart question suggestions, rich UI, dark theme |

---

## 🌟 Project Statement

Modern analysts drown in web articles, press releases, and blog posts. Copy-pasting text into ChatGPT works for a single page but fails when you need:

1. **Multiple sources combined** into one knowledge base.
2. **Repeatable Q&A** without losing context.
3. **Traceable answers** with clickable citations.

The **AI Research Tool** solves this by automatically:

1. Loading 1-3 article URLs.
2. Chunking text with LangChain.
3. Creating OpenAI embeddings and storing them in a local FAISS vector DB.
4. Allowing the user (or the app itself) to ask natural-language questions.
5. Returning answers *with exact source links* so you can verify every claim.

---

## Architecture
<img width="2400" height="1800" alt="9cc06003" src="https://github.com/user-attachments/assets/f191de59-5bb4-4953-8be4-44018a399228" />


---
## 📸 Screenshots

Enhanced UI
<img width="1826" height="860" alt="Screenshot 2025-08-18 033136" src="https://github.com/user-attachments/assets/47662e60-4d26-4afe-9867-dde79a77b2b9" />



Basic UI
<img width="1824" height="801" alt="Screenshot 2025-08-18 033358" src="https://github.com/user-attachments/assets/fe91bea3-5c00-4ebb-af67-8d136b9c0390" />

---

## 🗂️ Repository Structure

```text
.
├── main.py               # Basic Mode app
├── enhanced_main.py      # Enhanced Mode app
├── requirements.txt      # Locked Python dependencies
├── .gitignore            # Ignore venvs, secrets, FAISS indices, etc.
├── .env.example          # Template for your OpenAI key
├── .streamlit/
│   └── config.toml       # (optional) global dark theme tweaks
└── README.md             # ← this file
```

> FAISS indices are written to **`embeddings_folder/`** at runtime and are git-ignored.

---

## 🔎 Feature Matrix

| Category | Basic Mode (`main.py`) | Enhanced Mode (`enhanced_main.py`) |
|----------|-----------------------|------------------------------------|
| Max URLs | 3 | 3 |
| URL Loader | ✅ UnstructuredURLLoader | ✅ |
| FAISS + OpenAI Embeddings | ✅ | ✅ |
| Ad-hoc Q&A | ✅ | ✅ |
| Auto-generate 6 contextual questions | ❌ | **✅** |
| Tabs (Input / Analysis / Custom) | ❌ | **✅** |
| Dark theme & gradient header | ❌ | **✅** |
| Collapsible "How to Use" panel | ❌ | **✅** |
| Clickable source links | Basic plain text | **Styled buttons (new tab)** |
| Debug preview of indexed text | ❌ | ✅ |
| Reset / Clear session button | ❌ | ✅ |

---

## ✈️ Quick Start (Local)

```bash
# 1. clone & enter directory
git clone https://github.com/<your-user>/ai-research-tool.git
cd ai-research-tool

# 2. set up virtual env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. install deps
pip install -r requirements.txt

# 4. add your OpenAI key
cp .env.example .env
echo "OPENAI_API_KEY=sk-..." >> .env

# 5. run either version
streamlit run main.py            # basic
streamlit run enhanced_main.py   # enhanced
```

---

## 🛰️ Deploying **two apps** on Streamlit Cloud (Free Tier)

1. **Push** this repo to GitHub.
2. Log in to <https://share.streamlit.io> with the same GitHub account.
3. **App #1 – Core**
   * Repo: `your-user/ai-research-tool`
   * Branch: `main`
   * File: `main.py`
   * Add secret `OPENAI_API_KEY`.
4. **App #2 – Enhanced**
   * Same repo and branch
   * File: `enhanced_main.py`
   * Same secret
5. Click **Deploy** for each. You now have **two live URLs** from one repo.

> **Free-tier limits**: 1 GB RAM, 1 CPU, sleeps after a week of inactivity.

---

## 🛠️ How to Use – Enhanced Mode

1. **Enter URLs** in *Content Input* tab.
2. Click **Analyze Content** – progress spinners show stage.
3. Switch to *AI Analysis* tab.
4. Click **Analyze** next to any suggested question **or** ask your own in *Custom Questions*.
5. Answers appear with highlighted citations; links open in a new tab.
6. Use **Clear Analysis** in the sidebar to reset session and delete local FAISS index.

### Debug Mode
Enable the *Debug Mode* checkbox (Options panel) to preview the exact chunked text that is embedded.

---

## 🧩 Internals

| Step | Library | File / Class |
|------|---------|--------------|
| Load HTML → text | `langchain_community.document_loaders.UnstructuredURLLoader` | both apps |
| Split to 1 000-char chunks | `RecursiveCharacterTextSplitter` | both apps |
| Embeddings | `OpenAIEmbeddings` (`text-embedding-3-large`) | both apps |
| Vector DB | `FAISS` (saved to `embeddings_folder/`) | both apps |
| Retrieval + QA | `RetrievalQA.from_chain_type("stuff")` | both apps |
| Auto-question prompt | custom prompt in `generate_suggested_questions()` | enhanced only |

---

## ⚠️ Limitations & Future Work

* **3-URL cap** keeps latency low; future work could add paging and async loading.
* Indices stored locally; a remote DB (e.g.
  DeepLake, Elasticsearch) would support unlimited docs.
* Streamlit free tier is single-user; scale-out would require a separate backend.

---

## 🤝 Contributing

1. Fork the repo.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit & push; open PR.
4. Respect **MIT License** and add tests where possible.

---

## 📄 License

Released under the MIT License. See `LICENSE` for details.
