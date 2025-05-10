from google.adk.agents import  BaseAgent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from prompts.web_scrape_single_page_prompt import web_scrape_single_page_prompt
from typing import  List

from documentations.examples.serper_scrape_single_page_tool import serper_scrape_single_page_tool


def get_web_scrape_single_page_agent() -> LlmAgent:
    web_serach_agent = LlmAgent(
        name="web_search_agent",
        description="an agent the can scrape a single page from the web and return the results in a structured JSON format",
        instruction=web_scrape_single_page_prompt,
        model="gemini-2.0-flash",
        tools=[serper_scrape_single_page_tool],
      
     
        
       
        )
    return web_serach_agent

