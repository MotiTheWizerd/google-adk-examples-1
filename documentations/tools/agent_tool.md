# Agent Tool Documentation

## Overview

The `AgentTool` is a sophisticated wrapper that enables an agent to be used as a tool within a larger application. It bridges the gap between agents and tools, allowing for hierarchical agent structures and complex agent-to-agent interactions.

## Class Definition

```python
class AgentTool(BaseTool):
    def __init__(self, agent: BaseAgent, skip_summarization: bool = False):
        self.agent = agent
        self.skip_summarization: bool = skip_summarization
        super().__init__(name=agent.name, description=agent.description)
```

## Key Features

- Wraps any `BaseAgent` as a callable tool
- Automatic schema inference from agent's input/output specifications
- State and artifact propagation between parent and child agents
- Support for both structured and unstructured inputs
- Isolated execution environment with dedicated services

## Usage

### Basic Initialization

```python
from google.adk.agents import Agent
from google.adk.tools import AgentTool

# Create a sub-agent
calculator_agent = Agent(
    name="calculator",
    description="Performs mathematical calculations",
    model="gemini-2.0-flash"
)

# Wrap it as a tool
calculator_tool = AgentTool(agent=calculator_agent)

# Use in a parent agent
parent_agent = Agent(
    name="master",
    model="gemini-2.0-flash",
    tools=[calculator_tool]
)
```

### With Input/Output Schemas

```python
from pydantic import BaseModel

class CalculatorInput(BaseModel):
    operation: str
    numbers: list[float]

class CalculatorOutput(BaseModel):
    result: float
    steps: list[str]

calculator_agent = Agent(
    name="calculator",
    description="Performs mathematical calculations",
    model="gemini-2.0-flash",
    input_schema=CalculatorInput,
    output_schema=CalculatorOutput
)

calculator_tool = AgentTool(agent=calculator_agent)
```

## Technical Details

### Input Processing

1. **Structured Input (with schema)**:

   - Input is validated against the agent's input schema
   - Converted to JSON for agent consumption
   - Supports both dict and model instance inputs

2. **Unstructured Input**:
   - Accepts simple string input via the 'request' parameter
   - No validation beyond string type checking

### State Management

- Creates an isolated session for the wrapped agent
- Propagates state changes back to the parent context
- Maintains state consistency across agent hierarchy

### Artifact Handling

- Automatically forwards artifacts from child to parent session
- Preserves artifact naming and content
- Enables resource sharing between agents

### Service Isolation

Each wrapped agent gets its own:

- In-memory session service
- In-memory memory service
- Shared artifact service with parent

## Best Practices

1. **Schema Usage**:

   - Define input/output schemas for structured interactions
   - Use clear, descriptive schema fields
   - Validate complex data structures

2. **State Management**:

   - Keep state changes minimal and focused
   - Document state dependencies
   - Clear state when no longer needed

3. **Error Handling**:
   - Handle both schema validation errors
   - Manage state propagation failures
   - Validate input/output consistency

## Example: Complex Agent Hierarchy

```python
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from pydantic import BaseModel

# Define schemas
class ResearchQuery(BaseModel):
    topic: str
    depth: int
    focus_areas: list[str]

class ResearchResult(BaseModel):
    summary: str
    findings: list[str]
    references: list[str]

# Create specialized agents
researcher = Agent(
    name="researcher",
    description="Conducts detailed research",
    model="gemini-2.0-flash",
    input_schema=ResearchQuery,
    output_schema=ResearchResult
)

fact_checker = Agent(
    name="fact_checker",
    description="Verifies research findings",
    model="gemini-2.0-flash"
)

# Create tools from agents
research_tool = AgentTool(agent=researcher)
fact_check_tool = AgentTool(agent=fact_checker)

# Create orchestrator agent
orchestrator = Agent(
    name="research_manager",
    description="Manages research process",
    model="gemini-2.0-flash",
    tools=[research_tool, fact_check_tool]
)
```

## Limitations

1. Cannot share memory service between parent and child
2. Requires careful state management in complex hierarchies
3. May have performance overhead with deep agent nesting

## Related Components

- Works with any `BaseAgent` implementation
- Integrates with ADK's service architecture
- Compatible with all ADK tool features

## See Also

- [Agent Documentation](../agents/base_agent.md)
- [Tool Context Documentation](tool_context.md)
- [Service Architecture Documentation](../architecture/services.md)
