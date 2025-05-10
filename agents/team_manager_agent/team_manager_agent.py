from google.adk.agents import  BaseAgent, LlmAgent
from prompts.team_manager_prompt import team_manager_prompt
from typing import  List 


def get_team_manager(sub_agents: List[BaseAgent]  = []) -> LlmAgent:
    manager_agent = LlmAgent(
        name=team_manager_prompt["name"],
        description=team_manager_prompt["description"],
        instruction=team_manager_prompt["instruction"],
        model="gemini-2.0-flash",
        sub_agents=sub_agents,
        
       
        )
    return manager_agent

