# Built-in Code Execution Tool Documentation

## Overview

The `BuiltInCodeExecutionTool` is a specialized tool that enables code execution capabilities within Gemini 2 models. Unlike traditional code execution tools, this is a model-native tool that operates internally within the model itself, without performing any local code execution.

## Class Definition

```python
class BuiltInCodeExecutionTool(BaseTool):
    def __init__(self):
        super().__init__(name='code_execution', description='code_execution')
```

## Key Features

- Native integration with Gemini 2 models
- Model-internal code execution capabilities
- No local code execution required
- Automatic configuration handling

## Usage

### Basic Integration

```python
from google.adk.tools import built_in_code_execution
from google.adk.agents import Agent

# Create an agent with code execution capability
agent = Agent(
    name="code_executor",
    model="gemini-2.0-pro",
    tools=[built_in_code_execution]
)
```

### Pre-configured Instance

The tool comes with a pre-configured singleton instance:

```python
from google.adk.tools import built_in_code_execution  # Pre-configured instance
```

## Technical Details

### Model Compatibility

- **Supported Models**:

  - Gemini 2.x series
  - Future Gemini versions that support code execution

- **Unsupported Models**:
  - Gemini 1.x series
  - Other model families

### Configuration

The tool automatically:

1. Verifies model compatibility
2. Initializes configuration if needed
3. Adds code execution capability to the model's tool set

### Implementation Notes

- Uses `types.ToolCodeExecution()` from the Google GenAI SDK
- Operates as a model-native tool
- Requires no additional setup beyond inclusion in the agent's tool list

## Best Practices

1. **Model Selection**:

   - Always use with Gemini 2.x or newer models
   - Verify model compatibility before deployment

2. **Error Handling**:

   - Handle ValueError for unsupported models
   - Implement fallback strategies for incompatible models

3. **Security Considerations**:
   - Remember that code execution happens within the model
   - No direct access to local system resources
   - Safe for production use as it's sandboxed within the model

## Example: Using Code Execution in an Agent

```python
from google.adk.tools import built_in_code_execution
from google.adk.agents import Agent

# Create an agent that can execute code
code_agent = Agent(
    name="python_helper",
    description="Helps with Python programming tasks",
    model="gemini-2.0-pro",
    tools=[built_in_code_execution]
)

# The agent can now execute code within its responses
response = await code_agent.run("""
    Can you help me sort this list in Python?
    numbers = [5, 2, 8, 1, 9, 3]
""")
```

## Limitations

1. Only works with Gemini 2.x and newer models
2. No access to local system resources
3. Execution environment controlled by the model
4. Cannot interact with external services or files

## Error Messages

```python
# When using with unsupported model
ValueError: Code execution tool is not supported for model gemini-1.0-pro
```

## Related Components

- Integrates with ADK's agent system
- Works alongside other Gemini tools
- Compatible with ADK's tool management system

## See Also

- [Gemini Model Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Code Execution Safety](../security/code_execution.md)
- [Tool Context Documentation](tool_context.md)
