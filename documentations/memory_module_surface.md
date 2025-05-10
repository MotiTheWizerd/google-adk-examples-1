# ADK Memory Module: Public API & Surface Overview

## Purpose

This document summarizes the public API and main classes/functions of the `memory` module in the Agent Development Kit (ADK). It is intended as a reference for documentation and onboarding.

---

## What is Exposed (from `memory/__init__.py`)

- `BaseMemoryService`: Abstract base class for memory backends
- `InMemoryMemoryService`: Simple in-memory implementation (for prototyping/tests)
- `VertexAiRagMemoryService`: Vertex AI RAG-based implementation (for production, if dependencies are installed)

## Main Classes & Their Roles

### 1. `BaseMemoryService`

- **Description:** Abstract base class for all memory services in ADK.
- **Key Features:**
  - Defines the interface for adding sessions and searching memory
  - Uses Pydantic models for structured results (`MemoryResult`, `SearchMemoryResponse`)
- **Usage:** Inherit to create custom memory backends.

### 2. `InMemoryMemoryService`

- **Description:** Simple, non-persistent memory backend for prototyping and tests.
- **Key Features:**
  - Stores session events in a Python dictionary
  - Uses basic keyword matching for search (no semantic search)
  - Not suitable for production
- **Usage:** Good for local development, unit tests, or as a reference implementation.

### 3. `VertexAiRagMemoryService`

- **Description:** Production-ready memory backend using Google Vertex AI RAG for storage and semantic retrieval.
- **Key Features:**
  - Stores session events in a Vertex AI RAG corpus
  - Supports semantic search (vector similarity)
  - Handles merging of overlapping event lists
  - Requires Vertex AI dependencies; only available if installed
- **Usage:** Recommended for production or advanced use cases where persistence and semantic search are needed.

## Relationships

- All memory backends inherit from `BaseMemoryService`.
- The module exposes both simple (in-memory) and advanced (Vertex AI RAG) implementations.
- The public API is flexible: you can swap or extend memory backends as needed.
- Memory services are used by agents and workflows to store and retrieve session history.

---

## Extension Points: Creating Custom Memory Backends

The memory module is designed to be extensible. You can create your own memory backend by subclassing `BaseMemoryService`.

### How to Extend

1. **Subclass `BaseMemoryService`:**

   - Implement the following abstract methods:
     - `add_session_to_memory(self, session: Session)`
     - `search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse`
   - Use the provided Pydantic models (`MemoryResult`, `SearchMemoryResponse`) for structured results.

2. **Register or use your backend:**
   - You can instantiate your custom backend and use it wherever a memory service is needed (e.g., in agents, workflows, or tests).

### Minimal Example

```python
from google.adk.memory import BaseMemoryService, SearchMemoryResponse, MemoryResult
from google.adk.sessions.session import Session

class MyCustomMemoryService(BaseMemoryService):
    def add_session_to_memory(self, session: Session):
        # Your logic to store the session
        pass

    def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        # Your logic to search stored sessions
        # Return a SearchMemoryResponse with MemoryResult(s)
        return SearchMemoryResponse(memories=[])
```

### Tips & Best Practices

- Follow the interface: always return `SearchMemoryResponse` from `search_memory`.
- Use the `session.app_name`, `session.user_id`, and `session.id` fields for organizing data.
- If your backend is persistent or remote, handle errors and retries gracefully.
- Add docstrings and comments to help future maintainers.

---

## Next Steps / TODOs

- Document usage examples for each backend (in-memory, Vertex AI RAG)
- Explain extension points for custom memory backends
- Cross-link memory docs to agents, sessions, and tools
- Note any code comment/docstring gaps in the memory module

## Cross-References

- **Agents:** Memory services are used by agents to store and retrieve session history, enabling context continuity and smarter responses. See [agents_module_surface.md](agents_module_surface.md) for details on agent workflows and integration points.
- **Sessions & Events:** Memory backends operate on `Session` and `Event` objects. For more on their structure and lifecycle, see the sessions and events module documentation.
- **Tools:** Some built-in tools interact with memory (e.g., `load_memory`, `preload_memory`). See [tools_module_surface.md](tools_module_surface.md) for details on available tools and how they can leverage memory.

These cross-links help you navigate the ADK documentation and understand how memory fits into the overall agent development workflow.
