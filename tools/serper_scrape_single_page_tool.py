"""
Minimal Scraper Tool (ADK-compatible)
-------------------------------------

Scrapes a list of URLs by POSTing each to a configured scraper API root endpoint.
Provides both a plain function and an ADK FunctionTool for use in agents.

Requirements:
    - pip install requests
    - Set SCRAPER_API_URL in your environment (e.g., http://localhost:8000)
    - ADK agent: add `scraper_tool` to your tools list
"""
import os
import json
import requests
from typing import List, Dict, Any
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import FunctionTool

SCRAPER_API_URL = os.environ.get("SCRAPER_API_URL", "https://scrape.serper.dev")
SCRAPER_API_KEY = os.environ.get("SCRAPER_API_KEY", "44742fb5f61a502c7c85b72e71fa4a83fda9a325")

def serper_scrape_single_page_tool(urls: List[str], tool_context: ToolContext = None) -> str:
    """Scrape a list of URLs using the configured scraper API root endpoint.

    Args:
        urls (List[str]): List of URLs to scrape.
        tool_context (ToolContext, optional): ADK tool context.

    Returns:
        str: JSON string of results for each URL.
    """
    results: Dict[str, Any] = {}
    headers = {
        'X-API-KEY': SCRAPER_API_KEY,
        'Content-Type': 'application/json'
    }
    for url in urls:
        payload = json.dumps({"url": url})
        try:
            response = requests.post(SCRAPER_API_URL, headers=headers, data=payload, timeout=30)
            print(f"response for {url}: {response.text}")
            tool_context.state["scraped_urls_results"] = response.text
            response.raise_for_status()
            results[url] = response.json()
        except Exception as e:
            print(f"error for {url}: {e}")
            results[url] = {"error": str(e), "response": getattr(response, 'text', None)}
    return json.dumps(results)

# ADK FunctionTool for agent use
scraper_tool_adk = FunctionTool(serper_scrape_single_page_tool) 