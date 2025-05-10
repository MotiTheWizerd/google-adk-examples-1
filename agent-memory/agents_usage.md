## [2024-06-09] Correct Content Creation for LlmAgent

When creating a `types.Content` object for use with an `LlmAgent`, it is important to explicitly set `role="user"`:

```python
user_message = types.Content(role="user", parts=[types.Part(text="Find the latest news about AI agents.")])
```

**Problem:**
Omitting the `role` field can lead to the agent not recognizing the message as coming from the user, which may cause unexpected behavior or ignored input.

**Fix:**
Always set `role="user"` when constructing `types.Content` for user prompts.

**Lesson:**
Be explicit with the `role` field in `types.Content` to ensure proper agent context and message handling.

## [2024-06-09] Correct Content Creation for LlmAgent

When creating a `types.Content` object for use with an `LlmAgent`, it is important to explicitly set `role="user"`:

```python
user_message = types.Content(role="user", parts=[types.Part(text="Find the latest news about AI agents.")])
```

**Problem:**
Omitting the `role` field can lead to the agent not recognizing the message as coming from the user, which may cause unexpected behavior or ignored input.

**Fix:**
Always set `role="user"` when constructing `types.Content` for user prompts.

**Lesson:**
Be explicit with the `role` field in `types.Content` to ensure proper agent context and message handling.

## [2024-06-09] Explicit Session Creation Required in ADK InMemoryRunner

While testing the ADK agent framework, we encountered a `ValueError: Session not found` when running an agent with a session ID that hadn't been created. Investigation of the ADK source and docs revealed that sessions must be explicitly created using `session_service.create_session()` before use.

**Problem:** Attempting to run an agent with a non-existent session ID caused a runtime error.
**Fix:** Added a call to `runner.session_service.create_session()` before running the agent, using variables for `USER_ID` and a unique `SESSION_ID` generated with `uuid.uuid4()`.
**Lesson:** Always create sessions explicitly in ADK before use. Use uuid for session IDs to avoid collisions and improve maintainability. This pattern is common in agent frameworks and should be followed for robust, error-free code.

## [2024-06-09] LLM Agent Output Modification and Prompt Engineering Lessons

While building a manager agent (LlmAgent) that delegates to a tool agent (web_searcher_agent), we observed that the manager would summarize or modify the tool's output, even when instructed to return it "AS IS." This is due to LLM agents' default behavior of making responses more conversational or user-friendly.

**Problem:**
LLM agents tend to summarize, rephrase, or otherwise alter sub-agent/tool outputs unless explicitly told not to. Subtle instructions like "return AS IS" are often ignored, resulting in unwanted output changes.

**Fix:**
Added explicit, repetitive instructions to both the manager and tool agent prompts:

- "Don't modify the final response."
- "Don't summarize the final response."
- "Don't add any additional text to the final response."

This made the LLM agent pass through the tool's output unchanged.

**Lesson:**

- LLM agents require very explicit, repetitive instructions to enforce strict pass-through of tool/sub-agent results.
- Prompt-based control is fragile; for robust enforcement, consider programmatic solutions (e.g., serializing tool results as text, or bypassing the LLM layer for certain outputs).
- Printing each event and its author (agent name) during the run is invaluable for debugging and understanding where output is being changed or lost in the agent chain.

## [2024-06-09] Root Agent Name/Variable Mismatch Breaks Runner Recognition

While wiring up the root agent for the ADK runner, we named the variable `search` but set the agent's `name` property to `search_manager_agent`. Passing `search` to `InMemoryRunner` caused the runner and memory/session logic to fail to recognize the manager as the true root agent. This led to missing final responses and fallback behavior, because the project could not identify the correct manager in the agent hierarchy.

**Problem:** The root agent's variable name did not match its `name` property, breaking agent recognition in the runner/memory/session system.

**Fix:** Ensure the variable used to instantiate and register the root agent matches the agent's `name` property (e.g., both should be `search_manager_agent`).

**Lesson:** In ADK/agent frameworks, always keep the variable name and the agent's `name` property in sync when registering with runners or memory/session services. Otherwise, the system may not recognize the agent as the true manager/root, leading to subtle bugs in event routing and final response handling.
