"""
Network System Agent
--------------------
This agent is responsible for collecting, analyzing, and providing recommendations
on the system's network configuration.
It uses an LLM guided by a detailed prompt and a specialized network information tool.
"""
from google.adk.agents import LlmAgent
from prompts.network_system_agent_prompt import network_system_agent_prompt
from tools.network_info_tool import get_network_info # Import the ADK tool object

def get_network_system_agent() -> LlmAgent:
    """
    Factory function to create an instance of the NetworkSystemAgent.

    This agent uses an LLM to interpret network data gathered by the
    network_info_adk_tool and provide analysis and recommendations based
    on the instructions in network_system_agent_prompt.

    Returns:
        LlmAgent: An instance of the LlmAgent configured for network analysis.
    """
    agent = LlmAgent(
        name="network_system_agent",
        description="An agent that retrieves network information, analyzes it, and provides actionable recommendations.",
        instruction=network_system_agent_prompt,
        model="gemini-2.0-flash", # Or your preferred/default model for agents
        tools=[get_network_info],
        output_key="network_analysis_report" # Defines the key in the output where the agent's structured response will be found.
    )
    return agent 