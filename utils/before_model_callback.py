"""
before_model_callback.py

Utility callback for ADK LlmAgent to print the name of the LLM model before invocation.
References: Gemini LLM Provider, ADK callback conventions.
"""

def before_model_callback(callback_context, llm_request):
    """
    ADK-compatible before_model_callback that prints the LLM model name.
    Args:
        callback_context: ADK CallbackContext (not used here, but required by signature)
        llm_request: ADK LlmRequest, contains the model name
    Returns:
        None (does not short-circuit the model call)
    """
    agent_name = getattr(callback_context._invocation_context.agent, 'name', None)
    print(f"[before_model_callback] Agent name: {agent_name}")
    return None 