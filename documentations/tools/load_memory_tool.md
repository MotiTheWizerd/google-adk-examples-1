# LoadMemoryTool Documentation

## Overview

The `LoadMemoryTool` is a specialized tool in the ADK framework that enables agents to access and query the memory system. It extends the `FunctionTool` class and provides a mechanism for retrieving stored memories based on semantic queries.

## Class Definition

```python
class LoadMemoryTool(FunctionTool):
    """A tool that loads the memory for the current user."""
```

## Key Features

1. **Memory Retrieval**

   - Provides semantic search capability over stored memories
   - Returns relevant memories based on query strings
   - Integrates with the ADK memory service system

2. **LLM Integration**

   - Automatically informs the model about memory access capabilities
   - Provides clear instructions for memory querying
   - Seamlessly integrates with the LLM request pipeline

3. **Function Declaration**
   - Exposes a simple query-based interface
   - Uses standardized schema for parameter definition
   - Maintains compatibility with the ADK function tool system

## Usage

### Basic Usage

```python
# The tool is typically used through an LLM agent
agent = LlmAgent(
    tools=[load_memory_tool]
)

# The LLM can then use the tool with queries like:
response = load_memory("What was discussed about project timelines?")
```

### Parameters

- `query` (str): The search query to find relevant memories
  - Can be a natural language question
  - Supports semantic search capabilities
  - Returns memories that best match the query

### Return Value

- Returns a list of `MemoryResult` objects containing:
  - Relevant memory entries matching the query
  - Associated metadata and timestamps
  - Original conversation context

## Integration with Memory Service

The tool works in conjunction with the ADK memory service system:

1. Receives queries through the tool interface
2. Forwards searches to the underlying memory service
3. Returns formatted results to the agent

## Best Practices

1. **Query Formulation**

   - Use specific, focused queries for better results
   - Include relevant context in the query
   - Consider temporal aspects when searching memories

2. **Memory Management**
   - Regularly verify memory availability
   - Handle cases where no memories match
   - Consider memory service initialization

## Example Scenarios

1. **Conversation Context Retrieval**

   ```python
   # Retrieving previous discussion context
   memories = load_memory("What was previously discussed about the API design?")
   ```

2. **Decision History Lookup**
   ```python
   # Finding past decisions
   memories = load_memory("What was decided about the database schema?")
   ```

## Implementation Details

The tool is implemented with the following key components:

1. **Function Wrapper**

   ```python
   def load_memory(query: str, tool_context: ToolContext) -> 'list[MemoryResult]':
       response = tool_context.search_memory(query)
       return response.memories
   ```

2. **Function Declaration**

   ```python
   def _get_declaration(self) -> types.FunctionDeclaration:
       return types.FunctionDeclaration(
           name=self.name,
           description=self.description,
           parameters=types.Schema(
               type=types.Type.OBJECT,
               properties={
                   'query': types.Schema(
                       type=types.Type.STRING,
                   )
               },
           ),
       )
   ```

3. **LLM Request Processing**
   - Adds memory-related instructions to LLM context
   - Ensures the model knows how to use the memory system
   - Maintains consistent memory access patterns

## Error Handling

The tool includes built-in error handling for common scenarios:

- Memory service unavailability
- Invalid query formats
- Empty result sets

## Related Components

- `MemoryService`: Underlying storage and retrieval system
- `ToolContext`: Provides memory service access
- `LlmRequest`: Handles model interaction and instruction management
