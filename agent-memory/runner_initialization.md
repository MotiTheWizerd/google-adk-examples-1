## [2024-06-09] Runner Initialization Requires Main Agent Instance

When initializing an ADK runner (e.g., `InMemoryRunner`), it's essential to pass the main agent (manager/root agent) as an **object instance**, not as a string name. Passing a string (e.g., `"search_manager_agent"`) will cause a Pydantic validation error, since the runner expects an agent object (subclass of `BaseAgent`). In a previous project, a string variable was used, but it was resolved to the actual agent object before being passed to the runner, which is why it worked.

**Problem:**  
Passing a string as the agent argument to the runner causes a validation error and prevents the agent framework from running.

**Fix:**  
Always pass the agent instance (e.g., `agent=search_manager_agent`) to the runner. If using a string variable for flexibility, resolve it to the actual agent object before passing it.

**Lesson:**  
The runner requires the main agent as an object, not a string. Always ensure the correct type is provided during initialization to avoid runtime errors.
