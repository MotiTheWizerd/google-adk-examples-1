from adk.tools.tool_context import ToolContext


def exit_loop(tool_context : ToolContext):
    """
    This tool should be called when the agent wants to exit a loop,
    indicating that all tasks within that loop are completed.
    """
    tool_context.actions.escalate = True
