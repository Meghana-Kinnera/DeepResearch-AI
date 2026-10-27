# 🔍 DeepResearch-AI: Autonomous Multi-Agent Research Assistant

An autonomous multi-agent research engine built using **Python, Google Gemini AI, DuckDuckGo Web Search, and Streamlit**. It mimics human research workflows by breaking down complex topics into targeted search queries, retrieving web data, extracting verified facts with citations, and synthesizing comprehensive markdown reports.

---

## 🏗️ Architecture & Agent Breakdown

```
[ User Prompt / Topic ]
           │
           ▼
┌──────────────────────────────────────────────┐
│  1. Planner Agent                            │
│  Generates 3-5 sub-queries (Research Strategy)│
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  2. Search & Scraper Agent                   │
│  Performs web searches & scrapes web pages   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  3. Analyst Agent                            │
│  Extracts facts, statistics & source links   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  4. Report Writer Agent                      │
│  Drafts publication-ready Markdown report    │
└──────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
DeepResearch-AI/
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py   # Strategy & Query Generator
│   ├── search_agent.py    # Search execution & Web retriever
│   ├── analyst_agent.py   # Fact synthesis & Citations
│   └── writer_agent.py    # Final Markdown report compiler
├── tools/
│   ├── __init__.py
│   └── search_tool.py     # DuckDuckGo Search & Web Scraper
├── config.py              # Configuration & Gemini setup
├── pipeline.py            # Workflow Coordinator
├── app.py                 # Streamlit UI App
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
└── README.md              # Documentation
```

---

## 🚀 Quick Setup & Installation

### 1. Install Dependencies
Open terminal or command prompt in the project directory:
```bash
cd C:\Users\vamsi\OneDrive\Desktop\Projects\DeepResearch-AI
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the root folder (or copy from `.env.example`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> Get a free Gemini API Key at [Google AI Studio](https://aistudio.google.com/).
*(Note: You can also enter your API key directly in the UI sidebar).*

### 3. Run the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌟 Key Features
- **Zero-Cost Web Search:** Uses DuckDuckGo search engine (no paid search API required).
- **Multi-Agent Collaboration:** Sequential agent workflow with specialized prompts.
- **Fact Extraction & Citations:** Preserves original web page URLs for source attribution.
- **Real-Time Progress Tracking:** Live status logs showing current agent actions.
- **Export Formats:** Download reports as `.md` or `.txt` files.

---

## 💼 How to Present this in Interviews / Resume

- **Title:** DeepResearch-AI: Multi-Agent Deep Research System
- **Key Points:**
  - Designed and built an autonomous 4-agent pipeline using Python and Gemini 1.5 Flash.
  - Implemented automated research strategy generation, web searching/scraping, fact-verification, and structured report synthesis.
  - Built real-time streaming status UI using Streamlit.
