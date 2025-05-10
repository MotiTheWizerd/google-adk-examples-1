# CrewAI Tool Documentation

## Overview

The `CrewaiTool` is a wrapper class that enables seamless integration of CrewAI tools into the ADK framework. It extends `FunctionTool` and provides compatibility layer between CrewAI's tool system and ADK's tool infrastructure.

## Class Definition

```python
class CrewaiTool(FunctionTool):
    def __init__(self, tool: CrewaiBaseTool, *, name: str, description: str):
        super().__init__(tool.run)
        self.tool = tool
        # ... name and description handling ...
```

## Key Features

- Wraps CrewAI tools for use in ADK
- Preserves CrewAI tool functionality
- Automatic schema conversion
- Custom naming support
- Python 3.10+ compatibility

## Prerequisites

1. Python 3.10 or higher
2. ADK extensions package:
   ```bash
   pip install 'google-adk[extensions]'
   ```

## Usage

### Basic Integration

```python
from google.adk.tools import CrewaiTool
from crewai.tools import SerpAPI  # Example CrewAI tool

# Create a CrewAI tool
serpapi_tool = SerpAPI()

# Wrap it for ADK use
adk_serpapi = CrewaiTool(
    tool=serpapi_tool,
    name="web_search",
    description="Search the web using SerpAPI"
)

# Use in an ADK agent
agent = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    tools=[adk_serpapi]
)
```

### Using Default Names

```python
# CrewAI tool names are automatically converted:
# "Web Search" -> "web_search"
adk_serpapi = CrewaiTool(
    tool=serpapi_tool,
    name="",  # Will use converted CrewAI tool name
    description=""  # Will use CrewAI tool description
)
```

## Technical Details

### Name Handling

- Spaces in CrewAI tool names are replaced with underscores
- Names are converted to lowercase
- Custom names take precedence over CrewAI tool names

### Schema Conversion

- CrewAI tool schemas are automatically converted to ADK format
- Preserves parameter types and validation
- Maintains compatibility with both frameworks

### Function Declaration

The tool automatically:

1. Builds function declarations from CrewAI schemas
2. Converts parameter definitions
3. Preserves tool descriptions
4. Maintains argument validation

## Best Practices

1. **Naming**:

   - Use clear, descriptive custom names
   - Avoid spaces in custom names
   - Keep names consistent with ADK conventions

2. **Description Management**:

   - Provide ADK-specific descriptions when needed
   - Keep descriptions clear and concise
   - Include parameter information if not obvious

3. **Error Handling**:
   - Handle ImportError for Python version requirements
   - Verify CrewAI tool compatibility
   - Test wrapped tools thoroughly

## Example: Complex Integration

```python
from google.adk.tools import CrewaiTool
from crewai.tools import (
    SerpAPI,
    Calculator,
    WebsiteSearchTool
)
from google.adk.agents import Agent

# Create CrewAI tools
search_tool = SerpAPI()
calc_tool = Calculator()
website_tool = WebsiteSearchTool()

# Wrap tools with custom names and descriptions
adk_tools = [
    CrewaiTool(
        tool=search_tool,
        name="web_search",
        description="Search the web for current information"
    ),
    CrewaiTool(
        tool=calc_tool,
        name="calculator",
        description="Perform mathematical calculations"
    ),
    CrewaiTool(
        tool=website_tool,
        name="site_search",
        description="Search specific websites for information"
    )
]

# Create an agent with multiple CrewAI tools
research_agent = Agent(
    name="research_assistant",
    description="Assists with research using multiple tools",
    model="gemini-2.0-flash",
    tools=adk_tools
)

# Use the agent with CrewAI tools
response = await research_agent.run(
    "Research the latest AI developments and calculate their market impact"
)
```

## Limitations

1. Requires Python 3.10 or higher
2. Must install ADK extensions package
3. Some CrewAI tool features may not have direct ADK equivalents
4. Tool names must not contain spaces

## Error Messages

```python
# Python version error
ImportError: Crewai Tools require Python 3.10+. Please upgrade your Python version.

# Missing extension error
ImportError: Crewai Tools require pip install 'google-adk[extensions]'.
```

## Related Components

- Extends ADK's FunctionTool
- Integrates with CrewAI's tool system
- Compatible with ADK's agent framework

## See Also

- [CrewAI Documentation](https://docs.crewai.com/)
- [ADK Function Tool Documentation](function_tool.md)
- [ADK Extensions Guide](../extensions/index.md)
