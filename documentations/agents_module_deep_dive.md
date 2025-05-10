# ADK Agents Module Deep Dive Documentation

## Architectural Overview

The Agents module is the core of the ADK framework, providing a hierarchical, composable architecture for creating sophisticated AI agents. The module implements a tree-based structure that allows agents to work together in various patterns, from simple sequential workflows to complex hierarchical organizations.

### Core Architecture

```
┌────────────────────┐
│                    │
│   BaseAgent        │
│   (Abstract Base)  │
│                    │
└───────┬────────────┘
        │
        ├─────────────────────┬────────────────────┬────────────────────┐
        │                     │                    │                    │
┌───────▼──────────┐  ┌───────▼──────────┐ ┌───────▼──────────┐ ┌───────▼──────────┐
│                  │  │                  │ │                  │ │                  │
│   LlmAgent       │  │  SequentialAgent │ │  ParallelAgent  │ │  LoopAgent       │
│   (Main Agent)   │  │  (Orchestrator)  │ │  (Orchestrator) │ │  (Orchestrator)  │
│                  │  │                  │ │                  │ │                  │
└──────────────────┘  └──────────────────┘ └──────────────────┘ └──────────────────┘
```

The agent architecture follows a clear inheritance hierarchy:

1. **BaseAgent**: The abstract foundation that defines the core agent interface and functionality
2. **LlmAgent**: The workhorse of the framework, integrating LLM models with tools and specialized workflows
3. **Orchestrator Agents**: Special-purpose agents (Sequential, Parallel, Loop) that coordinate the execution of other agents in specific patterns

## Implementation Details

### BaseAgent Class

The `BaseAgent` class serves as the foundation for all agents, providing the critical infrastructure for agent management and execution:

```python
class BaseAgent(BaseModel):
    """Base class for all agents in Agent Development Kit."""

    name: str
    """The agent's name.

    Agent name must be a Python identifier and unique within the agent tree.
    Agent name cannot be "user", since it's reserved for end-user's input.
    """

    description: str = ''
    """Description about the agent's capability.

    The model uses this to determine whether to delegate control to the agent.
    One-line description is enough and preferred.
    """

    parent_agent: Optional[BaseAgent] = Field(default=None, init=False)
    """The parent agent of this agent."""

    sub_agents: list[BaseAgent] = Field(default_factory=list)
    """The sub-agents of this agent."""

    before_agent_callback: Optional[BeforeAgentCallback] = None
    """Callback signature that is invoked before the agent run."""

    after_agent_callback: Optional[AfterAgentCallback] = None
    """Callback signature that is invoked after the agent run."""
```

#### Key Methods

1. **Agent Execution**

   - `run_async`: The main entry point for text-based agent execution
   - `run_live`: Entry point for audio/video-based agent execution
   - `_run_async_impl`: Core implementation method to be overridden by subclasses
   - `_run_live_impl`: Core implementation method for live interactions

2. **Agent Navigation**

   - `root_agent`: Property that returns the topmost agent in the tree
   - `find_agent`: Finds an agent by name in the current subtree
   - `find_sub_agent`: Finds a direct descendant by name

3. **Context Management**
   - `_create_invocation_context`: Creates a proper context for the agent's execution
   - `__handle_before_agent_callback`: Manages pre-execution callbacks
   - `__handle_after_agent_callback`: Manages post-execution callbacks

### LlmAgent Class

The `LlmAgent` is the primary agent type in the framework, designed to integrate language models with tools and specialized execution patterns:

```python
class LlmAgent(BaseAgent):
    """LLM-based Agent."""

    model: Union[str, BaseLlm] = ''
    """The model to use for the agent.

    When not set, the agent will inherit the model from its ancestor.
    """

    instruction: Union[str, InstructionProvider] = ''
    """Instructions for the LLM model, guiding the agent's behavior."""

    global_instruction: Union[str, InstructionProvider] = ''
    """Instructions for all the agents in the entire agent tree."""

    tools: list[ToolUnion] = Field(default_factory=list)
    """Tools available to this agent."""

    generate_content_config: Optional[types.GenerateContentConfig] = None
    """The additional content generation configurations."""

    # Control configurations
    disallow_transfer_to_parent: bool = False
    disallow_transfer_to_peers: bool = False
    include_contents: Literal['default', 'none'] = 'default'

    # Schema constraints
    input_schema: Optional[type[BaseModel]] = None
    output_schema: Optional[type[BaseModel]] = None
    output_key: Optional[str] = None

    # Advanced features
    planner: Optional[BasePlanner] = None
    code_executor: Optional[BaseCodeExecutor] = None

    # Callbacks
    before_model_callback: Optional[BeforeModelCallback] = None
    after_model_callback: Optional[AfterModelCallback] = None
    before_tool_callback: Optional[BeforeToolCallback] = None
    after_tool_callback: Optional[AfterToolCallback] = None
```

#### Key Methods

1. **Model Resolution**

   - `canonical_model`: Resolves the model reference to a concrete LLM
   - `canonical_instruction`: Resolves static or dynamic instructions
   - `canonical_global_instruction`: Resolves global instruction settings
   - `canonical_tools`: Converts tool unions to actual tool instances

2. **Execution Flow**

   - `_llm_flow`: Determines whether to use a SingleFlow or AutoFlow based on agent configuration
   - `_run_async_impl`: Executes the LLM workflow in text-based mode
   - `_run_live_impl`: Executes the LLM workflow in live mode

3. **State Management**
   - `__maybe_save_output_to_state`: Handles output schema validation and state persistence

### Orchestrator Agents

The framework provides three specialized orchestration agents that manage the execution of other agents in specific patterns:

#### 1. SequentialAgent

```python
class SequentialAgent(BaseAgent):
    """A shell agent that run its sub-agents in sequence."""

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        for sub_agent in self.sub_agents:
            async for event in sub_agent.run_async(ctx):
                yield event
```

#### 2. ParallelAgent

```python
class ParallelAgent(BaseAgent):
    """A shell agent that run its sub-agents in parallel in isolated manner."""

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        _set_branch_for_current_agent(self, ctx)
        agent_runs = [agent.run_async(ctx) for agent in self.sub_agents]
        async for event in _merge_agent_run(agent_runs):
            yield event
```

#### 3. LoopAgent

```python
class LoopAgent(BaseAgent):
    """A shell agent that run its sub-agents in a loop."""

    max_iterations: Optional[int] = None
    """The maximum number of iterations to run the loop agent."""

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        times_looped = 0
        while not self.max_iterations or times_looped < self.max_iterations:
            for sub_agent in self.sub_agents:
                async for event in sub_agent.run_async(ctx):
                    yield event
                    if event.actions.escalate:
                        return
            times_looped += 1
```

## Agent Relationships and Tree Structure

ADK's agent architecture is fundamentally tree-based, with agents related in a parent-child hierarchy. This structure enables several powerful patterns:

1. **Model Inheritance**: Child agents can inherit model settings from their parents
2. **Context Propagation**: Execution contexts flow throughout the tree
3. **Escalation Paths**: Agents can escalate tasks upward in the hierarchy
4. **Delegation**: Parent agents can delegate tasks to their children

```
┌────────────────────┐
│                    │
│   Root Agent       │
│   (LlmAgent)       │──┐
│                    │  │
└────────────────────┘  │
                        │
                        │
┌────────────────────┐  │  ┌────────────────────┐
│                    │  │  │                    │
│  Orchestrator      │◄─┼──┤  Specialized       │
│  (SequentialAgent) │  │  │  (LlmAgent)        │
│                    │  │  │                    │
└──────────┬─────────┘  │  └────────────────────┘
           │            │
           │            │
┌──────────▼─────────┐ │  ┌────────────────────┐
│                    │ │  │                    │
│  Step 1            │ └─►│  Fallback          │
│  (LlmAgent)        │    │  (LlmAgent)        │
│                    │    │                    │
└──────────┬─────────┘    └────────────────────┘
           │
           │
┌──────────▼─────────┐
│                    │
│  Step 2            │
│  (LlmAgent)        │
│                    │
└────────────────────┘
```

## Integration Patterns

### 1. Simple LLM Agent

The most basic pattern - a single LLM agent with specific tools:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import google_search_tool

# Create a simple research assistant
research_agent = LlmAgent(
    name="researcher",
    model="gemini-2.0-flash",
    tools=[google_search_tool],
    instruction="""
    You are a research assistant that helps users find information online.
    Search the web to provide accurate, up-to-date information.
    """
)
```

### 2. Sequential Workflow

Breaking complex tasks into ordered steps with specialized agents:

```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search_tool, FunctionTool

# Create specialized agents for each step
researcher = LlmAgent(
    name="researcher",
    model="gemini-2.0-flash",
    tools=[google_search_tool],
    instruction="You research topics thoroughly and collect key facts."
)

analyzer = LlmAgent(
    name="analyzer",
    model="gemini-2.0-flash",
    instruction="You analyze research findings and identify patterns or insights."
)

writer = LlmAgent(
    name="writer",
    model="gemini-2.0-flash",
    instruction="You write clear, engaging content based on analysis."
)

# Combine into a sequential workflow
report_workflow = SequentialAgent(
    name="report_generator",
    description="Generates comprehensive reports through a multi-step process",
    sub_agents=[researcher, analyzer, writer]
)
```

### 3. Parallel Processing

Handling tasks that benefit from multiple independent approaches:

```python
from google.adk.agents import LlmAgent, ParallelAgent

# Create agents with different approaches
creative_agent = LlmAgent(
    name="creative_approach",
    model="gemini-2.0-flash",
    instruction="Generate creative, out-of-the-box solutions."
)

analytical_agent = LlmAgent(
    name="analytical_approach",
    model="gemini-2.0-flash",
    instruction="Generate analytical, structured solutions based on proven methods."
)

practical_agent = LlmAgent(
    name="practical_approach",
    model="gemini-2.0-flash",
    instruction="Generate practical, immediately implementable solutions."
)

# Run all approaches in parallel
solution_explorer = ParallelAgent(
    name="solution_explorer",
    description="Explores multiple solution paths simultaneously",
    sub_agents=[creative_agent, analytical_agent, practical_agent]
)
```

### 4. Iterative Refinement

Using a loop agent for tasks requiring iteration:

```python
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import FunctionTool

# Create a function to evaluate quality
def evaluate_quality(content: str) -> dict:
    """Evaluate the quality of content on a scale of 1-10."""
    # Evaluation logic here
    quality_score = 7  # Example score
    return {
        "score": quality_score,
        "feedback": "Content is good but could improve clarity in section 2."
    }

# Create the content creator agent
creator = LlmAgent(
    name="content_creator",
    model="gemini-2.0-flash",
    tools=[FunctionTool(evaluate_quality)],
    instruction="""
    You draft content and then improve it based on quality feedback.
    Use the evaluation tool to check quality and continue refining
    until you achieve a score of 9 or higher.
    """
)

# Wrap in a loop for iterative improvement
refiner = LoopAgent(
    name="iterative_refiner",
    description="Refines content through multiple iterations until quality thresholds are met",
    sub_agents=[creator],
    max_iterations=5  # Prevent infinite loops
)
```

### 5. Hierarchical Problem-Solving

Creating a hierarchical structure for complex problem domains:

```python
from google.adk.agents import LlmAgent, SequentialAgent

# Create a manager agent
manager = LlmAgent(
    name="project_manager",
    model="gemini-2.0-flash",
    instruction="""
    You oversee the entire project. You break down problems,
    delegate to specialists, and synthesize their outputs.
    """
)

# Create domain specialist agents
architect = LlmAgent(
    name="system_architect",
    model="gemini-2.0-flash",
    instruction="You design high-level system architecture and components."
)

developer = LlmAgent(
    name="developer",
    model="gemini-2.0-flash",
    instruction="You write code based on architectural specifications."
)

tester = LlmAgent(
    name="tester",
    model="gemini-2.0-flash",
    instruction="You test implementations and provide quality assurance."
)

# Create the hierarchical structure
project_team = SequentialAgent(
    name="software_team",
    description="A complete software development team with specialized roles",
    sub_agents=[
        manager,
        SequentialAgent(
            name="implementation_team",
            sub_agents=[architect, developer, tester]
        )
    ]
)
```

## Advanced Features

### 1. Callbacks for Monitoring and Modification

```python
from google.adk.agents import LlmAgent
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

# Define callbacks for monitoring and modifying LLM behavior
def before_model_hook(callback_context, llm_request: LlmRequest):
    """Pre-process model requests for logging or modification."""
    print(f"About to send request to {llm_request.model}")
    # Optionally modify the request
    return None  # Return None to proceed with normal model call

def after_model_hook(callback_context, llm_response: LlmResponse):
    """Process model responses for logging or modification."""
    print(f"Model generated {len(llm_response.texts)} text parts")
    # Optionally modify or replace the response
    return None  # Return None to use the original response

# Create agent with callbacks
monitored_agent = LlmAgent(
    name="monitored_agent",
    model="gemini-2.0-flash",
    instruction="You provide helpful responses.",
    before_model_callback=before_model_hook,
    after_model_callback=after_model_hook
)
```

### 2. Structured Input/Output

Using schemas to validate agent interactions:

```python
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent

# Define structured input schema
class ResearchQuery(BaseModel):
    topic: str = Field(..., description="Main research topic")
    focus_areas: list[str] = Field(..., description="Specific aspects to research")
    depth: str = Field(..., description="Research depth (brief, moderate, comprehensive)")

# Define structured output schema
class ResearchReport(BaseModel):
    summary: str = Field(..., description="Executive summary of findings")
    key_points: list[str] = Field(..., description="Key research points")
    sources: list[str] = Field(..., description="Information sources")
    confidence: float = Field(..., description="Confidence score (0-1)")

# Create agent with schema constraints
structured_agent = LlmAgent(
    name="structured_researcher",
    model="gemini-2.0-flash",
    instruction="You conduct research and produce structured reports.",
    input_schema=ResearchQuery,
    output_schema=ResearchReport,
    output_key="research_results"  # Store in session state with this key
)
```

### 3. Using a Planner for Complex Reasoning

```python
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

# Create a planner for step-by-step reasoning
planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        enable=True,
        verbosity=types.ThinkingVerbosity.HIGH
    )
)

# Create agent with planner
reasoning_agent = LlmAgent(
    name="reasoning_agent",
    model="gemini-2.0-flash",
    instruction="""
    You solve complex problems through careful step-by-step reasoning.
    Think through each step carefully before proceeding.
    """,
    planner=planner
)
```

### 4. Code Execution Integration

```python
from google.adk.agents import LlmAgent
from google.adk.code_executors import LocalCodeExecutor

# Create a code execution agent
coding_agent = LlmAgent(
    name="coding_assistant",
    model="gemini-2.0-flash",
    instruction="""
    You help users write and test Python code.
    When you provide code, it will be executed to verify it works correctly.
    """,
    code_executor=LocalCodeExecutor(
        allowed_imports=["math", "pandas", "numpy"],
        timeout_seconds=5
    )
)
```

## Performance Considerations

### 1. Model Sharing

Optimize performance by sharing models across agents:

```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models import LLMRegistry

# Create a shared model instance
shared_model = LLMRegistry.new_llm("gemini-2.0-flash")

# Create agents using the same model instance
agent1 = LlmAgent(
    name="agent1",
    model=shared_model,
    instruction="You handle the first part of the task."
)

agent2 = LlmAgent(
    name="agent2",
    model=shared_model,  # Same model instance
    instruction="You handle the second part of the task."
)

workflow = SequentialAgent(
    name="workflow",
    sub_agents=[agent1, agent2]
)
```

### 2. Strategic Tool Assignment

Distribute tools strategically across agents:

```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search_tool, load_memory_tool

# Create specialized agents with only necessary tools
researcher = LlmAgent(
    name="researcher",
    model="gemini-2.0-flash",
    tools=[google_search_tool],  # Only needs search
    instruction="You research topics and provide facts."
)

memory_agent = LlmAgent(
    name="memory_agent",
    model="gemini-2.0-flash",
    tools=[load_memory_tool],  # Only needs memory
    instruction="You recall previous conversations and maintain context."
)

workflow = SequentialAgent(
    name="workflow",
    sub_agents=[researcher, memory_agent]
)
```

### 3. Context Management

Optimize context handling for complex agent trees:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# Create a function to clean and summarize context
def summarize_context(conversation_history: str) -> dict:
    """Summarize lengthy conversation history to reduce context size."""
    # Summarization logic here
    return {"summary": "Condensed version of the conversation"}

# Create agent with context optimization
optimized_agent = LlmAgent(
    name="optimized_agent",
    model="gemini-2.0-flash",
    tools=[FunctionTool(summarize_context)],
    instruction="""
    For lengthy conversations, use the summarize_context tool
    to maintain essential information while reducing context size.
    """
)
```

## Error Handling and Debugging

### 1. Common Issues and Solutions

| Issue                      | Common Cause                    | Solution                                              |
| -------------------------- | ------------------------------- | ----------------------------------------------------- |
| Model inheritance failures | Missing model specification     | Ensure at least one ancestor has a specified model    |
| Agent name conflicts       | Duplicate agent names in tree   | Use unique, identifier-compliant names for all agents |
| Callback exceptions        | Errors in callback logic        | Add exception handling in all callback functions      |
| Schema validation errors   | Mismatched input/output formats | Carefully design schemas and ensure agent compliance  |
| Context propagation issues | Incorrect agent hierarchy       | Verify parent-child relationships are properly set    |

### 2. Debugging Techniques

```python
import logging
from google.adk.agents import LlmAgent

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("google.adk.agents")
logger.setLevel(logging.DEBUG)

# Add debugging callbacks
def debug_before_model(callback_context, llm_request):
    logger.debug(f"Agent: {callback_context.agent.name}")
    logger.debug(f"Request: {llm_request}")
    return None

def debug_after_model(callback_context, llm_response):
    logger.debug(f"Response: {llm_response}")
    return None

# Create a debuggable agent
debug_agent = LlmAgent(
    name="debug_agent",
    model="gemini-2.0-flash",
    instruction="You provide helpful responses.",
    before_model_callback=debug_before_model,
    after_model_callback=debug_after_model
)
```

## Security Considerations

### 1. Code Execution Sandboxing

```python
from google.adk.agents import LlmAgent
from google.adk.code_executors import LocalCodeExecutor

# Create a secure code execution environment
secure_executor = LocalCodeExecutor(
    allowed_imports=["math"],  # Only safe libraries
    timeout_seconds=2,  # Short timeout
    disallow_network_access=True,  # No network
    disallow_file_access=True,  # No file system
    memory_limit_mb=50  # Memory limit
)

# Create agent with secure code execution
secure_coding_agent = LlmAgent(
    name="secure_coder",
    model="gemini-2.0-flash",
    instruction="You write simple math utility functions.",
    code_executor=secure_executor
)
```

### 2. Tool Permission Controls

```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import (
    google_search_tool,
    load_memory_tool,
    example_tool
)

# Create agents with appropriate tool access
search_only_agent = LlmAgent(
    name="search_agent",
    model="gemini-2.0-flash",
    tools=[google_search_tool],  # Only search capability
    instruction="You can search for information online."
)

memory_only_agent = LlmAgent(
    name="memory_agent",
    model="gemini-2.0-flash",
    tools=[load_memory_tool],  # Only memory access
    instruction="You can recall past conversations."
)

# Orchestrate with controlled access
workflow = SequentialAgent(
    name="workflow",
    sub_agents=[search_only_agent, memory_only_agent]
)
```

### 3. Schema Validation for Security

```python
from pydantic import BaseModel, Field, validator
from google.adk.agents import LlmAgent

# Create a schema with security validations
class SecureInput(BaseModel):
    query: str = Field(..., description="User query")

    @validator("query")
    def sanitize_query(cls, value):
        # Simple sanitization example
        disallowed = ["--", ";", "DROP", "DELETE", "UPDATE"]
        for term in disallowed:
            if term.lower() in value.lower():
                raise ValueError(f"Query contains disallowed term: {term}")
        return value

# Create agent with secure input validation
secure_agent = LlmAgent(
    name="secure_agent",
    model="gemini-2.0-flash",
    instruction="You provide helpful information.",
    input_schema=SecureInput
)
```

## Future Considerations

### 1. Agent Evolution

As ADK continues to evolve, the agent architecture may incorporate new features:

- **Advanced Collaboration Patterns**: More sophisticated agent interaction models
- **Dynamic Agent Creation**: Runtime generation of agents based on task requirements
- **Learning Agents**: Agents that improve through feedback and experience
- **Agent Memory Optimization**: Better context management for complex agent hierarchies

### 2. Integration Opportunities

Future development directions may include:

- **Multi-Modal Agents**: Better support for vision, audio, and other input/output modalities
- **Cross-Framework Integration**: Deeper integration with other agent frameworks
- **Hybrid Human-AI Workflows**: More advanced patterns for human-in-the-loop scenarios
- **Distributed Agent Systems**: Support for agents distributed across multiple environments

## Conclusion

The Agents module is the heart of the ADK framework, providing powerful abstractions for building sophisticated AI systems that can tackle complex tasks through collaboration, delegation, and specialization. By leveraging the hierarchical agent architecture, developers can create systems that effectively combine the capabilities of large language models with specialized tools, structured workflows, and composition patterns to solve real-world problems.
