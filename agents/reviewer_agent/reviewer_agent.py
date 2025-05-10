"""
Reviewer Agent
--------------
This agent analyzes and synthesizes reports from other agents (system and network)
to provide a comprehensive, high-level overview, analysis, and consolidated recommendations.
It does not use any tools itself, relying on the input from preceding agents.
"""
from google.adk.agents import LlmAgent
from prompts.reviewer_agent_prompt import reviewer_agent_prompt

def get_reviewer_agent() -> LlmAgent:
    """
    Factory function to create an instance of the ReviewerAgent.

    This agent uses an LLM to interpret and synthesize information from the
    system_information and network_analysis_report provided in its input context.

    Returns:
        LlmAgent: An instance of the LlmAgent configured for reviewing and synthesizing reports.
    """
    agent = LlmAgent(
        name="reviewer_agent",
        description="A comprehensive reviewer agent that analyzes system and network reports to provide an integrated analysis and recommendations.",
        instruction=reviewer_agent_prompt,
        model="gemini-2.0-flash",  # Using a more capable model for synthesis might be beneficial
        tools=[],  # This agent does not use tools directly
        output_key="overall_review_report" # Defines the key for the agent's final output
    )
    return agent 