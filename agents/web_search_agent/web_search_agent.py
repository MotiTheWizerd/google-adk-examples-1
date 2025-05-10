from google.adk.agents import  BaseAgent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from prompts.web_search_prompt import web_search_prompt
from typing import  List
from tools.serper_search_tool import serper_search_tool



def get_web_search_agent(sub_agents: List[BaseAgent]  = []) -> LlmAgent:
    web_serach_agent = LlmAgent(
        name="web_search_agent",
        description="an agent that can search the internet using serper search tool for information and return the results in a structured JSON format",
        instruction=web_search_prompt,
        model="gemini-2.0-flash",
        sub_agents=sub_agents,
        tools=[serper_search_tool],
        output_key="web_results",
        
       
        )
    return web_serach_agent

