# agents.py
import os
import requests
from typing import Dict, Any, Optional, List

from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Optional: yfinance for stock data
try:
    import yfinance as yf
except Exception:
    yf = None

NEWSAPI_URL = "https://newsapi.org/v2/everything"

class DataCollector:
    """
    Fetch news + stock data for a given company (by name or ticker).
    If API keys/tools aren't available, uses dummy data.
    """

    def __init__(self, news_api_key: Optional[str] = None):
        self.news_api_key = news_api_key or os.getenv("NEWSAPI_KEY")

    def fetch_news(self, query: str, page_size: int = 5) -> List[Dict[str, Any]]:
        if not self.news_api_key:
            # Dummy fallback
            return [
                {"title": f"Sample headline about {query}", "description": f"Short description about {query}", "url": "https://example.com/news1"},
                {"title": f"Product launch for {query}", "description": "Company launched new product", "url": "https://example.com/news2"},
            ]
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": self.news_api_key,
        }
        resp = requests.get(NEWSAPI_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        return [{"title": a.get("title"), "description": a.get("description"), "url": a.get("url")} for a in articles]

    def fetch_stock(self, ticker: str, period: str = "1mo"):
        # Uses yfinance if installed and internet is available
        if yf is None:
            return {"error": "yfinance not available - returning dummy stock data", "prices": []}
        try:
            tk = yf.Ticker(ticker)
            hist = tk.history(period=period)
            # reduce to simple dict of date->close
            prices = [{"date": str(index.date()), "close": float(row["Close"])} for index, row in hist.iterrows()]
            return {"ticker": ticker, "prices": prices}
        except Exception as e:
            return {"error": str(e), "prices": []}

    def collect(self, company_name: str, ticker: Optional[str] = None) -> Dict[str, Any]:
        news = self.fetch_news(company_name, page_size=5)
        stock = self.fetch_stock(ticker or company_name, period="1mo") if ticker else {"prices": []}
        return {"company": company_name, "news": news, "stock": stock}
