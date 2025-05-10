from google.adk.agents import LlmAgent
from prompts.summarize_prompt import summarize_prompt

def get_summarize_agent() -> LlmAgent:
    return LlmAgent(
        name="summarize_agent",
        description="An agent that summarizes provided text or content into a concise, clear summary.",
        instruction=summarize_prompt,
        model="gemini-2.0-flash",
        tools=[],
        output_key="summary_result",
    ) 