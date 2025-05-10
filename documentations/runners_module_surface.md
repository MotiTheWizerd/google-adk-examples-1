# Runners Module Surface Overview

## Purpose

The `runners` module is responsible for orchestrating the execution of agents within the Agent Development Kit (ADK). It acts as the bridge between agents, session management, memory, and artifact storage, providing a unified interface for running agent workflows in both development and production environments.

## Main Responsibilities

- Manage the lifecycle of agent execution within a session
- Handle user input, event generation, and session updates
- Integrate with memory, session, and artifact services
- Support both synchronous and asynchronous agent runs
- Provide a simple in-memory runner for local testing and prototyping

## Key Classes

### Runner

- The core orchestrator for running agents
- Accepts an agent, session service, and optional memory/artifact services
- Main methods:
  - `run(...)`: Synchronous generator for local/testing
  - `run_async(...)`: Async generator for production/streaming
  - `run_live(...)`: Experimental live/streaming support
  - `close_session(...)`: Finalizes and persists session state

### InMemoryRunner

- Subclass of `Runner` for local development
- Wires up in-memory services for artifacts, sessions, and memory
- Requires only an agent to instantiate

## Integration Points

- **Agents:** Expects a `BaseAgent` (or subclass) as the main actor
- **Sessions:** Uses a session service to manage conversation history and state
- **Memory:** Optional memory service for persistent or advanced memory
- **Artifacts:** Optional artifact service for file/code/blob handling

## Extension & Customization

- Users can subclass `Runner` to implement custom orchestration or integrate with other backends
- All services (artifact, session, memory) are pluggable and can be swapped for custom implementations

## Cross-References

- See also: `agents`, `sessions`, `memory`, and `artifacts` modules for related extension points and integration details

## Extension Points & Customization

The `runners` module is designed for extensibility. Here are the main ways you can customize or extend runner behavior:

### 1. Subclassing `Runner`

- Implement custom orchestration logic (e.g., custom event handling, logging, or agent selection)
- Override methods like `run`, `run_async`, or internal helpers for advanced workflows
- Example:

```python
from google.adk.runners import Runner

class MyCustomRunner(Runner):
    def run(self, *args, **kwargs):
        # Add custom pre-processing
        print("Starting a custom run!")
        yield from super().run(*args, **kwargs)
        # Add custom post-processing
```

### 2. Plugging in Custom Services

- Provide your own implementations of artifact, session, or memory services
- Useful for integrating with databases, cloud storage, or external memory backends
- Example:

```python
runner = Runner(
    app_name="MyApp",
    agent=my_agent,
    artifact_service=MyCustomArtifactService(),
    session_service=MyCustomSessionService(),
    memory_service=MyCustomMemoryService(),
)
```

### 3. Advanced: Live/Streaming Extensions

- For real-time or streaming scenarios, extend or wrap `run_live` and related context logic
- See the `run_live` docstring and source for guidance

### Best Practices

- Favor composition (custom services) for most use-cases; subclass only for orchestration changes
- Keep custom runners well-documented and tested
- Cross-link your custom runner docs to related agent/session/memory docs for clarity

## Cross-References & Integration

- **Agents:** Runners require an agent (typically an `LlmAgent` or custom `BaseAgent` subclass) as the main actor. See the `agents` module for agent types, composition, and orchestration patterns.
- **Sessions:** All conversation state and event history is managed via a session service. See the `sessions` module for session models, storage, and extension points.
- **Memory:** Runners can use any `BaseMemoryService` implementation for persistent or advanced memory. See the `memory` module for built-in and custom memory backends.
- **Artifacts:** For workflows involving file/code/blob storage, plug in a custom or built-in artifact service. See the `artifacts` module for details and extension options.

For best results, cross-reference your custom runner or service docs with these related modules to help users understand the full integration story.

---

This overview provides a foundation for documenting usage examples, extension points, and best practices for the runners module.
