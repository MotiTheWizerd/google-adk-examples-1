# LangchainTool Documentation

## Overview

The `LangchainTool` is a specialized adapter class that enables seamless integration of Langchain tools into the ADK framework. It extends the `FunctionTool` class and provides a wrapper around Langchain tools, making them compatible with ADK's tool system.

## Class Definition

```python
class LangchainTool(FunctionTool):
    """Use this class to wrap a langchain tool.

    If the original tool name and description are not suitable, you can override
    them in the constructor.
    """
```

## Key Features

1. **Langchain Tool Wrapping**

   - Wraps any Langchain tool to make it compatible with ADK
   - Preserves original tool names and descriptions when appropriate
   - Supports both BaseTool and conventional Langchain tools

2. **Flexible Tool Handling**

   - Handles both standard Langchain tools (inheriting from BaseTool)
   - Supports conventional tools following Langchain patterns
   - Allows overriding of names and descriptions for better integration

3. **Function Declaration Generation**
   - Automatically generates appropriate function declarations
   - Handles schema conversion between Langchain and ADK formats
   - Supports both simple and complex tool signatures

## Usage

### Basic Usage

```python
from langchain.tools import BaseTool
from google.adk.tools import LangchainTool

# Wrap a Langchain tool
langchain_tool = some_langchain_tool()  # Your Langchain tool
adk_tool = LangchainTool(langchain_tool)

# Use in an ADK agent
agent = LlmAgent(tools=[adk_tool])
```

### With Custom Names/Descriptions

```python
# Override tool name and description if needed
langchain_tool = some_langchain_tool()
adk_tool = LangchainTool(langchain_tool)
adk_tool.name = "custom_name"
adk_tool.description = "Custom description for better clarity"
```

## Implementation Details

### Tool Types Support

The tool handles two main types of Langchain tools:

1. **BaseTool Implementation**

   - Tools that inherit from `langchain.tools.BaseTool`
   - Full schema and argument support
   - Preserves tool metadata

2. **Convention-based Tools**
   - Tools that don't inherit but follow Langchain conventions
   - Must have a `run` method
   - Basic function wrapping support

### Function Declaration Generation

The tool automatically generates appropriate function declarations by:

- Using the tool's schema if available (for BaseTool)
- Creating a basic declaration for conventional tools
- Preserving argument structures and types

## Best Practices

1. **Tool Naming**

   - Use clear, descriptive names when overriding defaults
   - Maintain consistency with ADK naming conventions
   - Consider the context where the tool will be used

2. **Schema Handling**

   - Verify schema compatibility when wrapping complex tools
   - Test with sample inputs before deployment
   - Handle any schema conversion edge cases

3. **Error Handling**
   - Implement proper error handling in wrapped tools
   - Test both success and failure scenarios
   - Provide clear error messages

## Integration Examples

### With Standard Langchain Tool

```python
from langchain.tools import DuckDuckGoSearchTool
from google.adk.tools import LangchainTool

# Create and wrap a search tool
search_tool = DuckDuckGoSearchTool()
adk_search = LangchainTool(search_tool)

# Use in agent
agent = LlmAgent(tools=[adk_search])
```

### With Custom Langchain Tool

```python
from langchain.tools import BaseTool
from google.adk.tools import LangchainTool

class CustomLangchainTool(BaseTool):
    name = "custom_tool"
    description = "A custom tool implementation"

    def _run(self, query: str) -> str:
        # Tool implementation
        return f"Processed: {query}"

# Wrap and use the custom tool
custom_tool = CustomLangchainTool()
adk_custom = LangchainTool(custom_tool)
```

## Limitations and Considerations

1. **Compatibility**

   - Not all Langchain tool features may be fully supported
   - Complex schemas might require additional handling
   - Some tool-specific features might not translate directly

2. **Performance**

   - Consider the overhead of tool wrapping
   - Test performance with large-scale operations
   - Monitor resource usage in production

3. **Maintenance**
   - Keep track of Langchain version compatibility
   - Update wrapped tools when Langchain updates
   - Test integration after significant updates

## Related Components

- `FunctionTool`: Base class for function-based tools
- `ToolboxTool`: Used in conjunction for tool management
- `BaseTool`: ADK's base tool class

## Future Considerations

- Enhanced schema conversion capabilities
- Better support for async Langchain tools
- Improved error handling and debugging
- Extended support for Langchain-specific features
