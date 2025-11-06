# Company Intelligence Agentic System (LangChain)

## Overview
Three-agent system:
- DataCollector: fetches news & stock (NewsAPI + yfinance fallback)
- Analyst: LLM-based summarization & insights (LangChain + OpenAI)
- Orchestrator: runs pipeline & persists conversation memory

## Setup
1. Clone repo
2. `pip install -r requirements.txt`  
3. Create `.env` or set:
   - `OPENAI_API_KEY` (required)
   - `NEWSAPI_KEY` (optional, for real news)
4. Run:
   - CLI demo: `python orchestrator.py`
   - Streamlit UI: `streamlit run streamlit_app.py`

## Files
- agents.py — DataCollector
- analyst.py — LLM Analyst
- orchestrator.py — Orchestrator & memory
- streamlit_app.py — simple UI
- notebook_demo.ipynb — example notebook

## Notes
- If `NEWSAPI_KEY` or `yfinance` are not available, the system uses dummy data so you can test LLM behavior offline.
- Replace `OpenAI` config/model in `analyst.py` if you want a different model or provider.
