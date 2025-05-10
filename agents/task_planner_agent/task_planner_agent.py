from dataclasses import Field
from google.adk.agents import  BaseAgent, LlmAgent
from google.adk.tools import BaseTool
from prompts.task_planner_prompt import task_planner_prompt
from agents.task_planner_agent.task_planner_agent import task_planner_agent
from typing import Dict, List # Added for older Python versions, though 3.9+ dict is fine.


def get_task_planner_agent(sub_agents: List[BaseAgent]  = []) -> LlmAgent:
    task_planner_agent = LlmAgent(
        name=task_planner_prompt["name"],
        description=task_planner_prompt["description"],
        instruction=task_planner_prompt["instruction"],
        model="gemini-2.0-flash",
        sub_agents=sub_agents,
        )
    return task_planner_agent

