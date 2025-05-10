## [2024-06-09] Lessons from Debugging Agent Output Schema

**1. Pydantic v2 Strictness:**

- When initializing an agent (like `LlmAgent`), Pydantic v2 enforces strict type checking.
- Fields like `output_key` must be a string, not a list. Passing the wrong type (e.g., `['greeting']` instead of `'greeting'`) causes a validation error.

**2. output_schema Must Be a Pydantic Model Class:**

- The `output_schema` argument for `LlmAgent` must be a subclass of `BaseModel`, not a dictionary or instance.
- Passing a dict (even if it looks like a schema) results in a Pydantic validation error:
  `Input should be a subclass of BaseModel [type=is_subclass_of, ...]`
- The correct approach is to define a Pydantic model (e.g., `class GreetingOutput(BaseModel): greeting: str`) and pass the class itself.

**3. ADK and Pydantic Integration:**

- The ADK agent framework relies on Pydantic models for input/output validation and serialization.
- This enforces type safety and makes agent outputs predictable and testable.

**4. Debugging Approach:**

- Always check both the documentation and the actual ADK source code to confirm how fields are expected to be used.
- Error messages from Pydantic are clear and should be trusted for diagnosing type issues.

**Entities/Relationships/Observations:**

- Entity: `LlmAgent` (from ADK)
- Relationship: `output_key` must be a string; `output_schema` must be a Pydantic model class
- Observation: Pydantic v2's strict typing prevents common mistakes and enforces clean contracts between agents and their outputs

## [2024-06-20] Project Rule: Do Not Use input_schema

While implementing the manager agent, it was clarified that the project should not use the `input_schema` argument in agent definitions. This is a project-wide convention to keep agent interfaces simpler and avoid unnecessary schema validation at the agent level.

**Problem:** Used `input_schema` in a new agent, which is against project conventions.
**Fix:** Remove `input_schema` from all agent definitions going forward.
**Lesson:** Always check and follow project-specific conventions for agent configuration. In this project, avoid using `input_schema` in any agent setup.

## [2024-06-20] Practical Workflow Philosophy

- Agents should be easily composable, with clear separation of concerns (e.g., manager delegates, searcher searches).
- The team is open to quick iteration and prioritizes practical, working code over theoretical purity.
