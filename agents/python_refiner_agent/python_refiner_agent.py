from google.adk.agents import LlmAgent
from prompts.python_refiner_agent_prompt import python_refiner_agent_prompt

def get_python_refiner_agent() -> LlmAgent:
    """
    Factory function to create and configure the Python Refiner Agent.

    This agent analyzes Python code to find bugs, errors, and improve quality.
    It uses an LLM guided by a specific prompt to perform its tasks.
    The agent is expected to output a JSON structure indicating whether the code
    is satisfactory or needs further improvement, along with the refined code.
    """
    return LlmAgent(
        name="python_refiner_agent",
        description="An LLM-based agent that refines Python code by identifying/fixing errors and improving quality.",
        instruction=python_refiner_agent_prompt,
        # Consider making the model configurable or choosing one appropriate for code tasks
        model="gemini-2.0-flash", # Example model, choose appropriately
        tools=[], # No specific ADK tools for now, LLM handles refinement directly
        # The output_key helps in retrieving the raw JSON string output from the LLM
        output_key="refinement_details_json", 
    )