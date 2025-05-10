"""
System Information Agent
------------------------
This agent is responsible for collecting and providing system information.
It uses an LLM to process a request and the system_info_tool to gather data.
"""
from google.adk.agents import LlmAgent
from prompts.system_info_agent_prompt import system_info_agent_prompt
from tools.system_info_tool import get_system_info # Assuming this tool is registered or made available

# TODO: Ensure 'get_system_info' is properly exposed as an ADK tool object.
# For example, if tools.system_info_tool defines 'system_info_tool_object',
# import and use that instead:
# from tools.system_info_tool import system_info_tool_object
# tools=[system_info_tool_object]


def get_system_info_agent() -> LlmAgent:
    """
    Factory function to create an instance of the SystemInfoAgent.

    Returns:
        LlmAgent: An instance of the LlmAgent configured for system information.
    """
    agent = LlmAgent(
        name="system_info_agent",
        description="An agent that retrieves and presents system hardware and software information using available tools.",
        instruction=system_info_agent_prompt,
        model="gemini-2.0-flash", # Or your preferred model
        tools=[get_system_info], # This assumes get_system_info is directly usable or wrapped as an ADK tool object
        output_key="system_information" # Key for the structured output
    )
    return agent 