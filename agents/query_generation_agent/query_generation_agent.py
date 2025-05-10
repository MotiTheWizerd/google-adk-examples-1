from google.adk.agents import LlmAgent, BaseAgent
from typing import List
from prompts.query_generation_agent_prompt import query_generation_agent_prompt

# You can later replace this with a more advanced prompt or logic


def get_query_generation_agent(sub_agents: List[BaseAgent] = []) -> LlmAgent:
    agent = LlmAgent(
        name="query_generation_agent",
        description="An agent that converts user natural language into effective queries (search, database, etc.)",
        instruction=query_generation_agent_prompt,
        model="gemini-2.0-flash",
        sub_agents=sub_agents,
        tools=[],  # Add tools if needed for query validation or enrichment
        output_key="generated_query",
    )
    return agent 