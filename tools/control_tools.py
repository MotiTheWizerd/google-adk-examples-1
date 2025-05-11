from pydantic import BaseModel, Field
from google.adk.tools import ToolConfig

class ExitLoopInput(BaseModel):
    """Input schema for the exit_loop tool. It takes no parameters."""
    pass

exit_loop_tool = ToolConfig(\
    name="exit_loop",
    description="Call this tool when you are fully satisfied with the Python code after your review and believe no further improvements are necessary. This signals that the review process for the current code can conclude.",
    input_schema=ExitLoopInput,
    # No execute_tool function is needed here if the orchestrator handles the side effect
    # of exiting based on the tool call itself. If the tool needed to *do* something
    # within the ADK framework (e.g., return a specific value), we\'d define an execute_tool.
    # For signaling purposes, the name and invocation are key.
)

# To make it easily importable:
__all__ = ["exit_loop_tool"] 