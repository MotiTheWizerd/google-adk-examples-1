# Runners Module Usage Examples

This guide shows how to use the `Runner` and `InMemoryRunner` classes to run agents in the ADK. It covers basic usage, synchronous and asynchronous runs, and how to plug in custom services.

---

## 1. Using InMemoryRunner for Quick Prototyping

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

# Create your agent (replace with your own config)
agent = LlmAgent(name="EchoAgent", ...)

# Set up the in-memory runner
runner = InMemoryRunner(agent)

# Prepare a user message
user_message = types.Content(parts=[types.Part(text="Hello, agent!")])

# Run synchronously (for local/testing)
for event in runner.run(user_id="user1", session_id="sess1", new_message=user_message):
    print(event)

# Or run asynchronously (recommended for production)
import asyncio
async def main():
    async for event in runner.run_async(user_id="user1", session_id="sess1", new_message=user_message):
        print(event)

asyncio.run(main())
```

---

## 2. Using Runner with Custom Services

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.memory.vertex_ai_rag_memory_service import VertexAiRagMemoryService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.sessions.in_memory_session_service import InMemorySessionService

agent = LlmAgent(name="CustomAgent", ...)

runner = Runner(
    app_name="MyApp",
    agent=agent,
    artifact_service=InMemoryArtifactService(),
    session_service=InMemorySessionService(),
    memory_service=VertexAiRagMemoryService(...),
)

# Usage is the same as above
```

---

## 3. Experimental: Live/Streaming Usage

```python
# For advanced/experimental use-cases (e.g., audio streaming)
# See the docstring for Runner.run_live and related classes
```

---

**Tips:**

- Use `InMemoryRunner` for local dev, tests, and quick experiments.
- Use `Runner` with custom services for production or integration with external backends.
- All runners require an agent and a session/user context.
- Events yielded by runners can be used to update UIs, logs, or trigger downstream actions.
