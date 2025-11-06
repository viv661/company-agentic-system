# analyst.py
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, Any

class Analyst:
    """
    Uses an LLM to summarize data and produce insights and risk factors.
    """

    def __init__(self, model_name: str = "gpt-4o-mini" or "gpt-4o", temperature: float = 0.0):
        # use LangChain OpenAI wrapper - ensure OPENAI_API_KEY in env
        self.llm = OpenAI(model_name="gpt-4o-mini", temperature=temperature)

        template = """You are a company analyst.
Given the following data for {company}, produce:
1) A short executive summary (3-4 sentences).
2) Top 5 insights or trends.
3) Top 5 risk factors or watch items.
4) Suggested next steps for an investor or product manager.

Data:
News articles:
{news}

Stock data (last month close prices):
{stock}

Be concise, actionable, and label sections clearly.
"""
        self.prompt = PromptTemplate(input_variables=["company", "news", "stock"], template=template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def analyze(self, data: Dict[str, Any]) -> str:
        news_summ = "\n".join([f"- {a.get('title')}: {a.get('description')}" for a in data.get("news", [])])
        stock = data.get("stock", {})
        stock_str = ""
        if isinstance(stock, dict) and "prices" in stock and len(stock["prices"])>0:
            stock_points = stock["prices"][:5]
            stock_str = "\n".join([f"{p['date']}: {p['close']}" for p in stock_points])
        else:
            stock_str = "No stock price data available."

        result = self.chain.run({"company": data.get("company", "Unknown"), "news": news_summ, "stock": stock_str})
        return result
