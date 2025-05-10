# ADK Memory Module: Usage Examples

This guide shows how to use the two main memory backends in ADK: the in-memory backend (for prototyping/tests) and the Vertex AI RAG backend (for production/semantic search).

---

## 1. Using InMemoryMemoryService

```python
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions.session import Session
from google.adk.events.event import Event, Content, Part

# Create the memory service
memory = InMemoryMemoryService()

# Create a session with some events
session = Session(
    app_name="my_app",
    user_id="user123",
    id="session1",
    events=[
        Event(
            author="user123",
            timestamp=1716000000.0,
            content=Content(parts=[Part(text="Hello, how are you?")])
        ),
        Event(
            author="agent",
            timestamp=1716000001.0,
            content=Content(parts=[Part(text="I'm good, thanks!")])
        ),
    ]
)

# Add the session to memory
memory.add_session_to_memory(session)

# Search memory with a keyword query
response = memory.search_memory(app_name="my_app", user_id="user123", query="hello")

for memory_result in response.memories:
    print(f"Session: {memory_result.session_id}")
    for event in memory_result.events:
        print(f"  {event.author}: {event.content.parts[0].text}")
```

**Notes:**

- This backend is fast and easy for local dev or tests, but not persistent or scalable.
- Search is simple keyword matching (case-insensitive).

---

## 2. Using VertexAiRagMemoryService

```python
from google.adk.memory import VertexAiRagMemoryService
from google.adk.sessions.session import Session
from google.adk.events.event import Event, Content, Part

# You must have the Vertex AI SDK and dependencies installed.
# You also need a configured Vertex AI RAG corpus.

# Create the memory service (replace with your actual corpus name)
memory = VertexAiRagMemoryService(
    rag_corpus="projects/your-project/locations/us-central1/ragCorpora/your-corpus-id",
    similarity_top_k=5,
    vector_distance_threshold=10.0,
)

# Create a session (same as above)
session = Session(
    app_name="my_app",
    user_id="user123",
    id="session1",
    events=[
        Event(
            author="user123",
            timestamp=1716000000.0,
            content=Content(parts=[Part(text="Hello, how are you?")])
        ),
        Event(
            author="agent",
            timestamp=1716000001.0,
            content=Content(parts=[Part(text="I'm good, thanks!")])
        ),
    ]
)

# Add the session to memory
memory.add_session_to_memory(session)

# Search memory with a semantic query
response = memory.search_memory(app_name="my_app", user_id="user123", query="greeting")

for memory_result in response.memories:
    print(f"Session: {memory_result.session_id}")
    for event in memory_result.events:
        print(f"  {event.author}: {event.content.parts[0].text}")
```

**Notes:**

- This backend uses semantic search (vector similarity), so queries can be more natural.
- Requires setup of Vertex AI RAG and the appropriate Python packages.
- Good for production, persistent, and large-scale use cases.

---

## See Also

- For more on sessions and events, see the `sessions/` and `events/` module docs.
- For extending memory, see the module surface overview and extension points.
