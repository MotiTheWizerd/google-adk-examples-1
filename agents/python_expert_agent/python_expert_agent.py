from google.adk.agents import BaseAgent, LlmAgent
from typing import List

# Import the prompt
from prompts.python_expert_agent_prompt import python_expert_agent_prompt

# Import any tools your agent might need (optional)
# For a Python expert agent, tools for code execution, linting, or file system access might be relevant in the future.
# from tools.your_specific_tool import your_specific_tool

def get_python_expert_agent(sub_agents: List[BaseAgent] = []) -> LlmAgent:
    """
    Factory function to create and configure the PythonExpertAgent.

    This agent acts as a senior Python developer. It receives a user request
    for Python code (e.g., functions, classes, scripts, debugging help)
    and returns the generated code in a structured JSON format.
    """

    agent_instruction = python_expert_agent_prompt
    agent_name = "python_expert_agent"
    agent_description = (
        "A senior expert Python developer agent that takes user requests "
        "and provides Python code solutions in JSON format."
    )

    python_expert_agent_instance = LlmAgent(
        name=agent_name,
        description=agent_description,
        instruction=agent_instruction,
        model="gemini-2.0-flash", # Using a more capable model for code generation
        tools=[
            # Add any relevant tools here in the future, e.g., a code execution tool.
        ],
        output_key="generated_code"
      
    )
    return python_expert_agent_instance

#late factorial."
 