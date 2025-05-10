## [2024-07-28] Pydantic Validation Error for list fields with None default

When creating a wrapper function that instantiates a Pydantic model, if the model expects a list for a field (e.g., `tools: list[BaseTool]`) and the wrapper function has a default parameter value of `None` for that field, a `pydantic_core.ValidationError` will occur if the wrapper is called without providing that argument. Pydantic expects a list, not `None`, unless the field is typed as `Optional[list[...]]` or has a `default_factory`.

**Problem:** `LlmAgent`'s `tools` and `sub_agents` fields (assumed to be `list`) were receiving `None` from `task_planner_agent`'s default parameters, causing a validation error.

**Fix:** Modified the `task_planner_agent` function signature to accept `Optional` lists (e.g., `tools: list[BaseTool] | None = None`). Then, within the function, when instantiating `LlmAgent`, explicitly pass an empty list `[]` if the argument is `None`:

```python
def task_planner_agent(llm: str = "gemini-2.0-pro", tools: list[BaseTool] | None = None, sub_agents: list[BaseAgent] | None = None):
    return LlmAgent(
        # ... other args
        tools=tools if tools is not None else [],
        sub_agents=sub_agents if sub_agents is not None else []
    )
```

**Lesson:** For Pydantic models, ensure that fields expecting a list receive a list. If a wrapper function provides defaults, make sure it either defaults to an empty list or converts `None` to an empty list before passing it to the Pydantic model constructor. This avoids `ValidationError` for list types.
