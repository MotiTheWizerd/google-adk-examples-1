# PreloadMemoryTool Documentation

## Overview

The `PreloadMemoryTool` is a specialized tool in the ADK framework that automatically preloads relevant memories based on the user's current query. Unlike most tools that are explicitly called, this tool works behind the scenes to enhance the LLM's context with relevant historical conversations.

## Class Definition

```python
class PreloadMemoryTool(BaseTool):
    """A tool that preloads the memory for the current user."""
```

## Key Features

1. **Automatic Memory Preloading**

   - Analyzes user's current query
   - Searches for relevant past conversations
   - Injects relevant memories into LLM context

2. **Contextual Enhancement**

   - Formats memories with timestamps
   - Preserves conversation structure
   - Maintains author attribution
   - Wraps memories in clear delimiters

3. **Silent Operation**
   - Works automatically without explicit invocation
   - Requires no direct interaction from the LLM
   - Seamlessly integrates with the request pipeline

## Implementation Details

### Memory Processing

The tool processes memories in the following way:

1. **Query Extraction**

   ```python
   parts = tool_context.user_content.parts
   if not parts or not parts[0].text:
       return
   query = parts[0].text
   ```

2. **Memory Search**

   ```python
   response = tool_context.search_memory(query)
   if not response.memories:
       return
   ```

3. **Memory Formatting**
   ```python
   memory_text = ''
   for memory in response.memories:
       time_str = datetime.fromtimestamp(memory.events[0].timestamp).isoformat()
       memory_text += f'Time: {time_str}\n'
       for event in memory.events:
           # Process each event in the memory
   ```

### Context Integration

The tool integrates memories into the LLM context using a structured format:

```
The following content is from your previous conversations with the user.
They may be useful for answering the user's current query.
<PAST_CONVERSATIONS>
[formatted memory content]
</PAST_CONVERSATIONS>
```

## Usage

### Automatic Integration

```python
# The tool is typically added to an agent's toolkit
agent = LlmAgent(
    tools=[preload_memory_tool]
)

# It will automatically process each request
# No explicit invocation needed
```

### Memory Format

Memories are formatted as follows:

```
Time: [ISO formatted timestamp]
[Author]: [Message content]
Time: [Next memory timestamp]
[Author]: [Message content]
...
```

## Best Practices

1. **Tool Placement**

   - Add early in the tool chain
   - Consider interaction with other memory tools
   - Ensure memory service is properly initialized

2. **Performance Considerations**

   - Monitor memory search performance
   - Consider limiting memory results
   - Be aware of context window limitations

3. **Content Handling**
   - Handle missing or malformed content gracefully
   - Respect multi-part content (future enhancement)
   - Maintain conversation context integrity

## Limitations and Future Enhancements

1. **Current Limitations**

   - Only supports single-part content
   - No filtering or prioritization of memories
   - Fixed formatting structure

2. **Planned Enhancements**
   - Support for multi-part content
   - Enhanced memory relevance scoring
   - Configurable formatting options

## Integration with Other Tools

The `PreloadMemoryTool` works well in combination with:

1. **LoadMemoryTool**

   - PreloadMemoryTool provides initial context
   - LoadMemoryTool allows explicit memory queries

2. **Other Context Tools**
   - Can be combined with artifact loading
   - Works alongside other context enhancement tools

## Error Handling

The tool includes robust error handling:

- Gracefully handles missing user content
- Skips processing when no memories are found
- Safely processes malformed memory entries

## Related Components

- `ToolContext`: Provides access to memory service
- `LlmRequest`: Target for memory injection
- `MemoryService`: Underlying memory storage system
- `LoadMemoryTool`: Companion tool for explicit memory access
