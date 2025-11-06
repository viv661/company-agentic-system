# orchestrator.py
import os
from langchain.memory import ConversationBufferMemory

from agents import DataCollector
from analyst import Analyst

class Orchestrator:
    def __init__(self, news_api_key: str = None):
        self.data_collector = DataCollector(news_api_key=news_api_key)
        self.analyst = Analyst()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def run_company_pipeline(self, company_name: str, ticker: str = None) -> dict:
        # Step 1: collect
        data = self.data_collector.collect(company_name, ticker)
        # Add to memory
        summary_entry = f"Collected data for {company_name}: {len(data.get('news', []))} news items, stock entries: {len(data.get('stock', {}).get('prices', []))}"
        self.memory.save_context({"input": f"collect {company_name}"}, {"output": summary_entry})

        # Step 2: analyze
        analysis_text = self.analyst.analyze(data)
        # Save analysis to memory
        self.memory.save_context({"input": f"analyze {company_name}"}, {"output": analysis_text})

        return {"data": data, "analysis": analysis_text, "memory": self.memory.load_memory_variables({})}

if __name__ == "__main__":
    # quick demo run
    news_api_key = os.getenv("NEWSAPI_KEY")
    orchestrator = Orchestrator(news_api_key=news_api_key)
    res = orchestrator.run_company_pipeline("OpenAI", ticker="MSFT")  # example
    print(res["analysis"])
