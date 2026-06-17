"""
web_search.py
Web search integration with Tavily/DuckDuckGo.
"""
import logging
import os
from typing import List, Dict

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

logger = logging.getLogger(__name__)

class WebSearcher:
    """Performs web search to augment generation context."""

    def __init__(self, provider: str = "tavily", api_key: str = None):
        self.provider = provider
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        logger.info(f"Searching web using {self.provider} for query: {query}")
        
        if self.provider == "tavily" and TavilyClient is not None and self.api_key:
            client = TavilyClient(api_key=self.api_key)
            response = client.search(query=query, max_results=max_results)
            return [
                {"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("content", "")}
                for r in response.get("results", [])
            ]
        
        logger.warning("Falling back to stub implementation (Tavily not configured).")
        return [
            {"title": "Stub result", "url": "https://example.com", "snippet": "Configure TAVILY_API_KEY to see real results."}
        ]
