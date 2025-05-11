from google.adk.agents import LlmAgent
from prompts.python_reviewer_agent_prompt import python_reviewer_agent_prompt
from utils.llm.exit_loop import exit_loop

def get_python_reviewer_agent() -> LlmAgent:
    """
    Factory function to create and configure the Python Code Reviewer Agent.

    This agent reviews Python code, identifies bugs, and suggests improvements.
    If satisfied with the code, it calls the 'exit_loop' tool.
    """
    return LlmAgent(
        name="python_reviewer_agent",
        description="An LLM-based agent that reviews Python code, suggests improvements, and can signal satisfaction by calling the 'exit_loop' tool.",
        instruction=python_reviewer_agent_prompt,
        model="gemini-2.0-flash", # Choose an appropriate model for code review tasks
        tools=[exit_loop], # Pass the exit_loop_tool to the agent
        # output_key can be used to get the raw text output (review comments)
        # when the agent doesn't call a tool.
        output_key="review_comments", 
    )

# Conceptual example of how an orchestrator might use this agent:
# (This would typically reside in a different part of the application)
#
# def example_orchestrator_for_reviewer(code_to_review: str, max_review_cycles: int = 1):
#     reviewer_agent = get_python_reviewer_agent()
#     current_code = code_to_review
#     loop_exited = False
#
#     for i in range(max_review_cycles): # Usually a reviewer might only run once per code version
#         print(f"--- Review Cycle {i + 1} ---")
#         try:
#             # Input to the agent is the code to review
#             agent_result_dict = reviewer_agent.execute(inputs={"text_input": current_code})
#
#             # Check if a tool was called
#             if agent_result_dict.get("tool_calls"):
#                 for tool_call in agent_result_dict["tool_calls"]:
#                     if tool_call["name"] == "exit_loop":
#                         print("INFO: Python Reviewer Agent called 'exit_loop'. Code is satisfactory.")
#                         # Actual exit_loop() logic/callback would be invoked here by the orchestrator
#                         loop_exited = True
#                         break
#                 if loop_exited:
#                     break
#             else:
#                 # If no tool call, get the review comments
#                 comments = agent_result_dict.get("review_comments", "No comments provided.")
#                 print("Reviewer Comments:")
#                 print(comments)
#                 # Here, an orchestrator might decide to pass these comments to another agent
#                 # (like the PythonRefinerAgent) or present them to a user.
#
#         except Exception as e:
#             print(f"ERROR: Error during review cycle: {e}")
#             break # Stop on error
#         
#         if loop_exited:
#             break
# 
#     if not loop_exited:
#         print("Review cycle(s) completed. 'exit_loop' was not called by the reviewer.")
#
#     return current_code # Or comments, or status, depending on orchestrator needs
#
# if __name__ == '__main__':
#     # Note: This __main__ block is for conceptual testing.
#     # Running it requires ADK setup and an active LLM service.
#
#     print("** Python Reviewer Agent Conceptual Test **")
#
#     code_needing_review = "def func1( a, b):
#         result =a+b # bad spacing, potential for type issues
#         print('result is '+result) # potential type error if a,b are not strings
#         return result"
#     # example_orchestrator_for_reviewer(code_needing_review)
#
#     excellent_code = "def add(a: int, b: int) -> int:\n    # Adds two integers and returns the sum.\n    return a + b\n"
#     # example_orchestrator_for_reviewer(excellent_code) 