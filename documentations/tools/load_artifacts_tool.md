# LoadArtifactsTool Documentation

## Overview

The `LoadArtifactsTool` is a specialized tool in the ADK framework that manages the loading and handling of artifacts within a session. It provides a mechanism for agents to access and work with artifacts stored in the session context.

## Class Definition

```python
class LoadArtifactsTool(BaseTool):
    """A tool that loads the artifacts and adds them to the session."""
```

## Key Features

1. **Artifact Management**

   - Loads artifacts from the session context
   - Maintains a list of available artifacts
   - Provides access to artifact content when requested

2. **LLM Integration**

   - Automatically informs the model about available artifacts
   - Handles artifact loading requests from the model
   - Manages artifact content in LLM requests

3. **Session Integration**
   - Works seamlessly with the ADK session system
   - Maintains artifact state within the session context
   - Provides consistent access to artifacts across interactions

## Usage

### Basic Usage

```python
from google.adk.tools import load_artifacts_tool

# The tool is pre-instantiated as a singleton
agent = LlmAgent(tools=[load_artifacts_tool])

# The tool will automatically handle artifact loading when needed
```

### Function Declaration

The tool exposes a simple interface to the LLM:

```python
{
    "name": "load_artifacts",
    "description": "Loads the artifacts and adds them to the session.",
    "parameters": {
        "type": "object",
        "properties": {
            "artifact_names": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }
}
```

## Implementation Details

### Artifact Loading Process

1. **Initialization**

   - Tool is initialized with a fixed name and description
   - No additional configuration required

2. **Function Declaration**

   - Defines a simple schema for artifact loading
   - Accepts an array of artifact names to load
   - Returns the list of loaded artifact names

3. **Request Processing**
   - Automatically appends available artifacts to LLM instructions
   - Handles artifact loading requests from the model
   - Attaches artifact content to LLM requests when needed

### Key Methods

1. **run_async**

   ```python
   async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any:
       artifact_names: list[str] = args.get('artifact_names', [])
       return {'artifact_names': artifact_names}
   ```

   - Processes artifact loading requests
   - Returns the list of requested artifact names

2. **process_llm_request**
   ```python
   async def process_llm_request(self, *, tool_context: ToolContext, llm_request: LlmRequest) -> None:
       # Handles LLM request processing and artifact attachment
   ```
   - Manages artifact information in LLM requests
   - Appends artifact content when requested

## Best Practices

1. **Artifact Management**

   - Keep artifact names descriptive and unique
   - Manage artifact lifecycle appropriately
   - Clean up unused artifacts when no longer needed

2. **Performance Considerations**

   - Be mindful of artifact sizes when loading
   - Consider caching strategies for frequently accessed artifacts
   - Monitor memory usage with large artifacts

3. **Error Handling**
   - Handle missing artifacts gracefully
   - Validate artifact names before loading
   - Provide clear error messages for troubleshooting

## Integration Examples

### Basic Artifact Loading

```python
from google.adk.tools import load_artifacts_tool

# Set up agent with the tool
agent = LlmAgent(
    tools=[load_artifacts_tool],
    # ... other configuration
)

# The tool will automatically handle artifact requests
# Example LLM prompt: "Please load and show me the content of artifact_1"
# The tool will automatically handle this request
```

### Working with Multiple Artifacts

```python
# The LLM can request multiple artifacts
# Example LLM function call:
{
    "name": "load_artifacts",
    "arguments": {
        "artifact_names": ["artifact_1", "artifact_2"]
    }
}
```

## Limitations and Considerations

1. **Memory Management**

   - Large artifacts can impact memory usage
   - Consider implementing size limits for artifacts
   - Monitor system resources when working with many artifacts

2. **Performance**

   - Loading multiple large artifacts may impact performance
   - Consider implementing lazy loading where appropriate
   - Monitor response times with large artifacts

3. **Security**
   - Validate artifact names and content
   - Implement access controls if needed
   - Consider artifact content sanitization

## Related Components

- `BaseTool`: Base class for all tools
- `ToolContext`: Provides session context and artifact management
- `LlmRequest`: Handles LLM communication and content management

## Future Considerations

1. **Enhanced Features**

   - Support for artifact filtering and searching
   - Improved artifact metadata handling
   - Advanced caching mechanisms

2. **Performance Optimizations**

   - Lazy loading of large artifacts
   - Improved memory management
   - Caching strategies

3. **Security Enhancements**
   - Better access control mechanisms
   - Content validation
   - Size and type restrictions

## Example Workflow

```python
# Example of how the tool works in a conversation flow

# 1. Agent setup
agent = LlmAgent(tools=[load_artifacts_tool])

# 2. User asks about available artifacts
# The tool automatically informs the LLM about available artifacts

# 3. LLM requests specific artifacts
# The tool loads and provides the content

# 4. LLM processes the artifact content
# The tool manages the artifact content in the conversation context
```

## Troubleshooting

1. **Common Issues**

   - Missing artifacts
   - Memory constraints
   - Performance bottlenecks

2. **Solutions**
   - Validate artifact existence before loading
   - Implement size limits and cleanup
   - Monitor and optimize performance

## See Also

- Session Management documentation
- Artifact handling best practices
- LLM integration guidelines
