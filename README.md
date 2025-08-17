# AI Research Tool 📰🔬

**Two Streamlit apps in one repo for rapid article analysis**

| App | Entry-point | Audience | Key idea |
|-----|-------------|----------|----------|
| **Core** | `main.py` | Minimal, lightning-fast demo | Paste URLs → vector index → ask questions |
| **Enhanced** | `enhanced_main.py` | Power users & portfolio showcase | Same engine + smart question suggestions, rich UI, dark theme |

---

![Architecture](chart:29)

> The pipeline shared by both apps: **URL → Loader → Text Splitter → FAISS + OpenAI Embeddings → Retrieval-QA → Answer + Sources**.

---

## 🌟 Features at a glance

| Capability | `main.py` | `enhanced_main.py` |
|-------------|-----------|--------------------|
| Load up to 3 article URLs | ✅ | ✅ |
| LangChain `UnstructuredURLLoader` | ✅ | ✅ |
| FAISS vector DB (local folder) | ✅ | ✅ |
| Ask ad-hoc questions | ✅ | ✅ |
| Auto-generate 6 contextual questions | ❌ | ✅ |
| Modern gradient header / dark mode | ❌ | ✅ |
| Tabs, cards, collapsible docs, debug preview | ❌ | ✅ |
| Clickable source links | Basic text | Styled, new-tab links |
| Session-state reset button | ❌ | ✅ |

---

## 📂 Repository layout

```
.
├── main.py               # core minimal app
├── enhanced_main.py      # richer UI + auto-questions
├── requirements.txt      # pinned python deps
├── .streamlit
│   └── config.toml       # optional theme tweaks
├── .env.example          # template for your OpenAI key
└── README.md             # ← you are here
```

> **Note** : FAISS indices are written to `embeddings_folder/`. Add that path to your `.gitignore`.

---

## 🚀 Quick start (local)

```bash
# clone
$ git clone https://github.com/<your-user>/ai-research-tool.git
$ cd ai-research-tool

# create venv & install
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt

# add your key
$ cp .env.example .env
$ echo "OPENAI_API_KEY=sk-..." >> .env

# run minimal app
$ streamlit run main.py

# in a second tab, try the enhanced version
$ streamlit run enhanced_main.py
```

---

## 🌐 Deploy both apps on Streamlit Cloud

> One repo ➜ many apps.  Streamlit Cloud lets you pick *file name* at deploy time.

1. **Push to GitHub**  
   ```bash
   git remote add origin https://github.com/<your-user>/ai-research-tool.git
   git add .
   git commit -m "initial push"
   git push -u origin main
   ```

2. **Create two Streamlit Cloud apps**  
   • **App 1 – Core**  
   ─ Repository: *ai-research-tool*  
   ─ Branch: `main`  
   ─ Main file: `main.py`
   
   • **App 2 – Enhanced**  
   ─ Same repository  
   ─ Main file: `enhanced_main.py`

3. **Set environment variable** `OPENAI_API_KEY` in **each** app’s *Secrets* tab:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```

4. *(Optional)* turn on **Always On** so FAISS indices persist between sleeps.

5. Press **Deploy**.  Each app gets its own URL, e.g.
   - `https://core-news-research.streamlit.app`  
   - `https://ai-research-tool.streamlit.app`

### ✍️ Updating
`git push` again ➜ Streamlit watches the repo ➜ both apps redeploy automatically.

---

## 🔧 Requirements
```
streamlit==1.34.0
langchain==0.2.3
langchain-community==0.2.3
faiss-cpu==1.8.0
python-dotenv==1.0.1
openai==1.33.0
unstructured==0.12.6
```

> Versions locked for repeatability.  Edit `requirements.txt` if you upgrade LangChain.

---

## 📈 Usage tips

| Tip | Why |
|------|-----|
| Preface URLs with `https://` | Loader ignores bare domains |
| Use 1-3 *high-quality* sources | Better embeddings = better answers |
| Delete `embeddings_folder/` occasionally | Keeps disk usage low on Cloud |
| Enable **Debug Mode** (Enhanced app) | See exactly which text was indexed |

---

## 🖼️ Illustrative screenshots

| Core (`main.py`) | Enhanced (`enhanced_main.py`) |
|:----------------:|:----------------------------:|
| ![core](attached_image:3) | ![enhanced](attached_image:4) |

*(Replace with fresh screenshots once deployed.)*

---

## 🤝 Contributing

Pull requests are welcome!  Feel free to submit issues for feature ideas or bug fixes.

---

## 📄 License

This project is released under the **MIT License** – see `LICENSE` for details.