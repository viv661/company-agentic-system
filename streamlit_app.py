# streamlit_app.py
import streamlit as st
from orchestrator import Orchestrator
import os

st.set_page_config(page_title="Company Intelligence Agent", layout="centered")
st.title("Company Intelligence Agentic System")

news_key = os.getenv("NEWSAPI_KEY")
orchestrator = Orchestrator(news_api_key=news_key)

company = st.text_input("Company name (or search query)", value="OpenAI")
ticker = st.text_input("Ticker symbol (optional)", value="")

if st.button("Run Pipeline"):
    with st.spinner("Collecting data & analyzing..."):
        out = orchestrator.run_company_pipeline(company, ticker or None)
    st.subheader("Analysis")
    st.write(out["analysis"])
    st.subheader("Collected News (titles)")
    for a in out["data"]["news"]:
        st.markdown(f"- **{a['title']}** — {a.get('description')}")
        st.markdown(f"[source]({a.get('url')})")
    st.subheader("Memory (recent)")
    st.json(out["memory"])
