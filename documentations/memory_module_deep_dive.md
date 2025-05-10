# ADK Memory Module Deep Dive Documentation

## Architectural Overview

The Memory module is a fundamental component of the ADK framework, providing persistent conversation history and semantic search capabilities. It enables agents to access past interactions, creating more contextually aware and coherent conversational experiences.

### Core Architecture

```
┌────────────────────┐
│                    │
│  BaseMemoryService │
│  (Abstract Base)   │
│                    │
└──────────┬─────────┘
           │
           ├─────────────────────┐
           │                     │
┌──────────▼─────────┐ ┌─────────▼───────────┐
│                    │ │                     │
│ InMemoryMemory     │ │ VertexAiRagMemory   │
│ Service            │ │ Service             │
│ (Prototype/Test)   │ │ (Production)        │
│                    │ │                     │
└────────────────────┘ └─────────────────────┘
```

The memory architecture follows a provider pattern with clear separation of concerns:

1. **BaseMemoryService**: The abstract foundation that defines the core memory interface
2. **InMemoryMemoryService**: A simple memory implementation for prototyping and testing
3. **VertexAiRagMemoryService**: A production-ready implementation using Vertex AI's RAG capabilities

## Core Components

### Memory Models

The memory module uses Pydantic models to provide structured data exchange:

```python
class MemoryResult(BaseModel):
  """Represents a single memory retrieval result.

  Attributes:
      session_id: The session id associated with the memory.
      events: A list of events in the session.
  """
  session_id: str
  events: list[Event]


class SearchMemoryResponse(BaseModel):
  """Represents the response from a memory search.

  Attributes:
      memories: A list of memory results matching the search query.
  """
  memories: list[MemoryResult] = Field(default_factory=list)
```

These models encapsulate:

- The session ID where the memory was found
- The relevant events (conversations) that match the query
- A structured container for multiple memory results

### BaseMemoryService

The `BaseMemoryService` class defines the core interface for all memory implementations:

```python
class BaseMemoryService(abc.ABC):
  """Base class for memory services.

  The service provides functionalities to ingest sessions into memory so that
  the memory can be used for user queries.
  """

  @abc.abstractmethod
  def add_session_to_memory(self, session: Session):
    """Adds a session to the memory service."""

  @abc.abstractmethod
  def search_memory(
      self, *, app_name: str, user_id: str, query: str
  ) -> SearchMemoryResponse:
    """Searches for sessions that match the query."""
```

This interface enforces:

1. **Session Storage**: A method to add session data to the memory store
2. **Memory Search**: A method to query stored memories by relevance to a query
3. **Consistent Response Format**: All implementations return the same structured data

## Implementation Details

### InMemoryMemoryService

The `InMemoryMemoryService` provides a lightweight, non-persistent implementation ideal for prototyping and testing:

```python
class InMemoryMemoryService(BaseMemoryService):
  """An in-memory memory service for prototyping purpose only.

  Uses keyword matching instead of semantic search.
  """

  def __init__(self):
    self.session_events: dict[str, list[Event]] = {}
    """keys are app_name/user_id/session_id"""

  def add_session_to_memory(self, session: Session):
    key = f'{session.app_name}/{session.user_id}/{session.id}'
    self.session_events[key] = [
        event for event in session.events if event.content
    ]

  def search_memory(
      self, *, app_name: str, user_id: str, query: str
  ) -> SearchMemoryResponse:
    # Implementation uses basic keyword matching
```

Key characteristics:

- Simple dictionary-based storage keyed by `app_name/user_id/session_id`
- Keyword-based search rather than semantic search
- Filters by app name and user ID to ensure data isolation
- No persistence between application restarts

### VertexAiRagMemoryService

The `VertexAiRagMemoryService` provides an enterprise-ready, persistent implementation using Google's Vertex AI RAG:

```python
class VertexAiRagMemoryService(BaseMemoryService):
  """A memory service that uses Vertex AI RAG for storage and retrieval."""

  def __init__(
      self,
      rag_corpus: str = None,
      similarity_top_k: int = None,
      vector_distance_threshold: float = 10,
  ):
    self.vertex_rag_store = types.VertexRagStore(
        rag_resources=[rag.RagResource(rag_corpus=rag_corpus)],
        similarity_top_k=similarity_top_k,
        vector_distance_threshold=vector_distance_threshold,
    )

  def add_session_to_memory(self, session: Session):
    # Implementation uploads session data to Vertex AI RAG

  def search_memory(
      self, *, app_name: str, user_id: str, query: str
  ) -> SearchMemoryResponse:
    # Implementation uses semantic search through Vertex AI RAG
```

Key characteristics:

- Configurable RAG corpus for storage and retrieval
- Vector-based semantic search (rather than just keywords)
- Configurable similarity thresholds and result limits
- Handles complex merging of related event sequences
- Requires Vertex AI dependencies

## Integration with Tool Ecosystem

The memory module integrates with ADK's tool ecosystem through specialized tools:

### 1. LoadMemoryTool

This tool enables agents to explicitly query memory when needed:

```python
class LoadMemoryTool(FunctionTool):
  """A tool that loads the memory for the current user."""

  def __init__(self):
    super().__init__(load_memory)

  @override
  async def process_llm_request(
      self,
      *,
      tool_context: ToolContext,
      llm_request: LlmRequest,
  ) -> None:
    # Adds instructions to inform the model about memory capability
```

Usage is straightforward for the agent:

```python
# Agent can call the tool with a query
memories = load_memory("previous conversation about taxes")
```

### 2. PreloadMemoryTool

This tool automatically preloads relevant memories into the model's context:

```python
class PreloadMemoryTool(BaseTool):
  """A tool that preloads the memory for the current user."""

  @override
  async def process_llm_request(
      self,
      *,
      tool_context: ToolContext,
      llm_request: LlmRequest,
  ) -> None:
    # Automatically searches memory based on current query
    # Formats and injects relevant memories into model context
```

This tool operates behind the scenes to:

1. Extract the user's current query
2. Search memory for relevant past conversations
3. Format those memories with timestamps and authors
4. Insert them into the model's context
