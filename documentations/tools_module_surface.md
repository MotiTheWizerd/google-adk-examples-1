# ADK Tools Module Documentation

## Overview

The Tools module is a fundamental component of the Agent Development Kit (ADK) that provides a collection of utility classes and functions designed to extend agent capabilities. It serves as the foundation for integrating various functionalities, APIs, and services into agent workflows.

### Key Concepts

- **Modularity**: Each tool is a self-contained unit that can be used independently or combined with other tools.
- **Extensibility**: The module follows a plugin-like architecture, making it easy to add new tools or customize existing ones.
- **Standardization**: All tools inherit from a common base class, ensuring consistent interfaces and behavior.
- **Integration-Ready**: Built-in support for various services and APIs, from Google Cloud to third-party frameworks.

### Core Features

- Function wrapping and parameter parsing
- API integrations (Google, OpenAPI, etc.)
- Memory management and retrieval
- Web interaction and data loading
- Agent-to-agent communication
- Long-running task handling
- User interaction management

## Module Structure and Components

### Core Tooling & Utilities

These tools form the foundation of the ADK tools system:

- **base_tool.py**

  - Purpose: Abstract base class defining the standard tool interface
  - Key Features: Common tool lifecycle management, error handling, context management

- **function_tool.py**

  - Purpose: Converts Python functions into ADK-compatible tools
  - Usage: Wrapping custom functions or external library functions

- **toolbox_tool.py**

  - Purpose: Groups related tools into manageable collections
  - Usage: Organizing and managing sets of related tools

- **tool_context.py**

  - Purpose: Manages execution context for tools
  - Features: State management, resource handling, cleanup

- **long_running_tool.py**
  - Purpose: Handles tools that require extended execution time
  - Features: Progress tracking, cancellation support

### Integration Tools

Tools for connecting with external services and frameworks:

- **Google Integration Tools**

  - google_search_tool.py: Web search capabilities
  - vertex_ai_search_tool.py: Vertex AI search integration
  - google_api_tool/: Various Google API integrations

- **AI/ML Framework Tools**

  - langchain_tool.py: LangChain integration
  - crewai_tool.py: CrewAI framework integration

- **Data and Memory Tools**
  - load_artifacts_tool.py: Artifact management
  - load_memory_tool.py: Memory operations
  - preload_memory_tool.py: Memory initialization
  - transfer_to_agent_tool.py: Inter-agent data transfer

### Specialized Tools

Tools for specific functionalities:

- **Web and API Tools**

  - load_web_page.py: Web content retrieval
  - openapi_tool/: OpenAPI specification handling
  - apihub_tool/: API hub integration

- **Execution Tools**
  - built_in_code_execution_tool.py: Safe code execution
  - exit_loop_tool.py: Loop control
  - get_user_choice_tool.py: User interaction

### Utility Directories

- **retrieval/**: Components for information retrieval
- **application_integration_tool/**: Application connectivity
- **mcp_tool/**: Multi-cloud platform integration

## Usage Guidelines

### Tool Selection Best Practices

1. Start with core tools for basic functionality
2. Add integration tools as needed for external services
3. Use specialized tools for specific requirements
4. Combine tools in toolboxes for related operations

### Common Patterns

1. Tool initialization and configuration
2. Error handling and recovery
3. Context management
4. Resource cleanup
5. Tool chaining and composition

## Detailed API Reference

### BaseTool (base_tool.py)

The `BaseTool` class serves as the abstract base class for all tools in the ADK system. It defines the standard interface and common functionality that all tools must implement.

#### Class Definition

```python
class BaseTool(ABC):
    name: str  # The name of the tool
    description: str  # The description of the tool
    is_long_running: bool = False  # Whether the tool is a long-running operation
```

#### Core Methods

1. **Constructor**

   ```python
   def __init__(self, *, name: str, description: str, is_long_running: bool = False)
   ```

   - Initializes a new tool instance
   - Parameters:
     - name: Tool identifier
     - description: Human-readable description
     - is_long_running: Flag for operations that don't complete immediately

2. **run_async**

   ```python
   async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any
   ```

   - Main execution method for the tool
   - Must be implemented by concrete tool classes
   - Parameters:
     - args: Arguments provided by the LLM
     - tool_context: Execution context
   - Returns: Tool execution result

3. **process_llm_request**

   ```python
   async def process_llm_request(self, *, tool_context: ToolContext, llm_request: LlmRequest) -> None
   ```

   - Processes outgoing LLM requests
   - Adds tool declarations to request configuration
   - Used for request preprocessing

4. **\_get_declaration**
   ```python
   def _get_declaration(self) -> Optional[types.FunctionDeclaration]
   ```
   - Returns OpenAPI specification for the tool
   - Used by default process_llm_request implementation
   - Can return None if not needed

#### Usage Example

```python
from google.adk.tools import BaseTool
from google.adk.tools import ToolContext

class MyCustomTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="A custom tool example",
            is_long_running=False
        )

    async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any:
        # Tool implementation here
        return result
```

#### Key Features

1. **Tool Lifecycle Management**

   - Standardized initialization
   - Async execution support
   - Context-aware operations

2. **LLM Integration**

   - OpenAPI specification support
   - Request preprocessing capabilities
   - Function declaration management

3. **Extensibility**
   - Abstract base class design
   - Flexible declaration system
   - Context-based execution

#### Best Practices

1. **Implementation**

   - Always implement run_async for client-side tools
   - Provide clear, descriptive names and descriptions
   - Handle long-running operations appropriately

2. **Context Usage**

   - Use tool_context for state management
   - Respect context lifecycle
   - Clean up resources properly

3. **LLM Integration**
   - Implement \_get_declaration when needed
   - Use process_llm_request for custom preprocessing
   - Follow OpenAPI specification guidelines

### FunctionTool (function_tool.py)

The `FunctionTool` class is a concrete implementation of `BaseTool` that wraps Python functions, making them available as ADK tools. This is one of the most commonly used tools as it provides a bridge between regular Python functions and the ADK tool system.

#### Class Definition

```python
class FunctionTool(BaseTool):
    func: Callable[..., Any]  # The wrapped Python function
```

#### Core Methods

1. **Constructor**

   ```python
   def __init__(self, func: Callable[..., Any])
   ```

   - Wraps a Python function as a tool
   - Uses function's name as tool name
   - Uses function's docstring as tool description

2. **run_async** (inherited from BaseTool)

   ```python
   async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any
   ```

   - Executes the wrapped function
   - Handles both sync and async functions
   - Validates mandatory arguments
   - Injects tool_context if function accepts it

3. **\_get_declaration** (inherited from BaseTool)
   ```python
   def _get_declaration(self) -> Optional[types.FunctionDeclaration]
   ```
   - Generates OpenAPI specification from function signature
   - Handles parameter types and descriptions
   - Excludes internal parameters (tool_context, input_stream)

#### Usage Example

```python
from google.adk.tools import FunctionTool

def greet(name: str, greeting: str = "Hello") -> str:
    """Generates a greeting message.

    Args:
        name: The name of the person to greet
        greeting: Optional custom greeting phrase

    Returns:
        A formatted greeting message
    """
    return f"{greeting}, {name}!"

# Create a tool from the function
greet_tool = FunctionTool(greet)
```

#### Key Features

1. **Automatic Function Wrapping**

   - Preserves function signature
   - Maintains docstring documentation
   - Handles default arguments
   - Supports type hints

2. **Argument Validation**

   - Checks for required parameters
   - Provides clear error messages
   - Handles optional arguments
   - Supports variable arguments

3. **Context Integration**
   - Optional tool_context injection
   - Streaming support
   - Async/sync function support

#### Best Practices

1. **Function Design**

   - Use clear, descriptive function names
   - Provide comprehensive docstrings
   - Use type hints for better OpenAPI generation
   - Handle both success and error cases

2. **Parameter Handling**

   - Define default values when appropriate
   - Document all parameters
   - Use meaningful parameter names
   - Consider validation requirements

3. **Return Values**
   - Return meaningful data structures
   - Handle errors gracefully
   - Consider return type consistency
   - Document return value format

#### Common Patterns

1. **Basic Function Wrapping**

   ```python
   def my_function(param1: str, param2: int = 42) -> dict:
       """Function description here."""
       return {"result": f"{param1}: {param2}"}

   tool = FunctionTool(my_function)
   ```

2. **Context-Aware Function**

   ```python
   async def context_aware(message: str, tool_context: ToolContext) -> str:
       """Uses tool context in processing."""
       session_id = tool_context.session_id
       return f"Processing {message} in session {session_id}"

   tool = FunctionTool(context_aware)
   ```

3. **Error Handling**

   ```python
   def careful_function(important_param: str) -> dict:
       """Handles errors gracefully."""
       try:
           result = process(important_param)
           return {"success": True, "data": result}
       except Exception as e:
           return {"success": False, "error": str(e)}

   tool = FunctionTool(careful_function)
   ```

### ToolboxTool (toolbox_tool.py)

The `ToolboxTool` class provides a way to manage and access collections of tools from a toolbox service. It acts as a client interface for loading individual tools or sets of tools from a remote toolbox server.

#### Class Definition

```python
class ToolboxTool:
    toolbox_client: Any  # The underlying toolbox client instance
```

#### Core Methods

1. **Constructor**

   ```python
   def __init__(self, url: str)
   ```

   - Initializes a connection to a toolbox service
   - Parameters:
     - url: The URL of the toolbox service (e.g., "http://127.0.0.1:5000")

2. **get_tool**

   ```python
   def get_tool(self, tool_name: str) -> LangchainTool
   ```

   - Retrieves a single tool from the toolbox
   - Parameters:
     - tool_name: Name of the tool to load
   - Returns: A LangchainTool wrapper around the loaded tool

3. **get_toolset**
   ```python
   def get_toolset(self, toolset_name: str) -> list[LangchainTool]
   ```
   - Retrieves a set of related tools
   - Parameters:
     - toolset_name: Name of the toolset to load
   - Returns: List of LangchainTool instances

#### Usage Example

```python
from google.adk.tools import ToolboxTool

# Initialize the toolbox client
toolbox = ToolboxTool("http://127.0.0.1:5000")

# Get a single tool
search_tool = toolbox.get_tool("search")

# Get a set of related tools
data_processing_tools = toolbox.get_toolset("data_processing")
```

#### Key Features

1. **Remote Tool Management**

   - Connects to toolbox services
   - Loads tools on demand
   - Supports tool collections

2. **LangChain Integration**

   - Wraps tools as LangchainTools
   - Compatible with LangChain workflows
   - Maintains tool interfaces

3. **Flexible Access**
   - Individual tool loading
   - Bulk toolset loading
   - URL-based configuration

#### Best Practices

1. **Service Configuration**

   - Use appropriate service URLs
   - Handle connection errors
   - Consider security implications
   - Validate tool availability

2. **Tool Management**

   - Group related tools in toolsets
   - Use meaningful tool names
   - Document tool dependencies
   - Version tools appropriately

3. **Integration Patterns**
   - Load tools lazily when needed
   - Cache frequently used tools
   - Handle tool loading failures
   - Monitor tool usage

#### Common Patterns

1. **Basic Tool Loading**

   ```python
   toolbox = ToolboxTool("http://localhost:5000")

   # Load individual tools
   calculator = toolbox.get_tool("calculator")
   translator = toolbox.get_tool("translator")
   ```

2. **Working with Toolsets**

   ```python
   # Load a complete set of related tools
   nlp_tools = toolbox.get_toolset("natural_language_processing")

   # Use tools from the set
   for tool in nlp_tools:
       # Configure and use each tool
       pass
   ```

3. **Error Handling**
   ```python
   try:
       toolbox = ToolboxTool("http://toolbox-server:5000")
       tool = toolbox.get_tool("critical_tool")
   except Exception as e:
       # Handle connection or loading errors
       logger.error(f"Failed to load tool: {e}")
       # Provide fallback behavior
   ```

#### Integration Notes

- Requires a running toolbox service
- Tools are loaded as LangchainTool instances
- Consider network reliability and latency
- Tool availability depends on server configuration

### ToolContext (tool_context.py)

The `ToolContext` class provides the execution context for tools in the ADK system. It extends `CallbackContext` and serves as a bridge between tools and the broader ADK environment, offering access to authentication, artifacts, memory, and event management.

#### Class Definition

```python
class ToolContext(CallbackContext):
    invocation_context: InvocationContext  # The tool's invocation context
    function_call_id: Optional[str]  # Identifier for the current function call
    event_actions: Optional[EventActions]  # Event management interface
```

#### Core Methods

1. **Constructor**

   ```python
   def __init__(self, invocation_context: InvocationContext, *,
                function_call_id: Optional[str] = None,
                event_actions: Optional[EventActions] = None)
   ```

   - Initializes a tool context
   - Parameters:
     - invocation_context: The execution context
     - function_call_id: Optional identifier for function calls
     - event_actions: Optional event management interface

2. **Authentication Methods**

   ```python
   def request_credential(self, auth_config: AuthConfig) -> None
   def get_auth_response(self, auth_config: AuthConfig) -> AuthCredential
   ```

   - Manage authentication flows
   - Handle credential requests and responses
   - Support various authentication configurations

3. **Artifact Management**

   ```python
   def list_artifacts(self) -> list[str]
   ```

   - Lists artifacts in the current session
   - Returns filenames of attached artifacts
   - Requires initialized artifact service

4. **Memory Operations**
   ```python
   def search_memory(self, query: str) -> SearchMemoryResponse
   ```
   - Searches user memory
   - Requires initialized memory service
   - Returns structured search results

#### Usage Example

```python
from google.adk.tools import ToolContext
from google.adk.auth import AuthConfig

class MyTool(BaseTool):
    async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any:
        # Authentication example
        auth_config = AuthConfig(type="oauth2", ...)
        tool_context.request_credential(auth_config)
        credential = tool_context.get_auth_response(auth_config)

        # Memory search example
        search_results = tool_context.search_memory("relevant query")

        # Artifact listing example
        available_artifacts = tool_context.list_artifacts()

        return {"results": process_data(search_results, available_artifacts)}
```

#### Key Features

1. **Authentication Management**

   - Credential request handling
   - Auth response processing
   - Multiple auth config support
   - Secure credential management

2. **Resource Access**

   - Artifact management
   - Memory service integration
   - Event action handling
   - Context state management

3. **Integration Support**
   - Callback context extension
   - Invocation context access
   - Function call tracking
   - Event system integration

#### Best Practices

1. **Authentication Handling**

   - Always check auth requirements
   - Handle auth failures gracefully
   - Use appropriate auth configs
   - Protect sensitive credentials

2. **Resource Management**

   - Check service availability
   - Handle missing services gracefully
   - Clean up resources properly
   - Monitor resource usage

3. **Error Handling**
   - Validate service states
   - Handle missing contexts
   - Provide meaningful errors
   - Implement proper fallbacks

#### Common Patterns

1. **Basic Context Usage**

   ```python
   async def run_tool(tool_context: ToolContext):
       # Access invocation context
       session_id = tool_context._invocation_context.session.id
       user_id = tool_context._invocation_context.user_id

       # Use context for operations
       results = await process_with_context(session_id, user_id)
       return results
   ```

2. **Authentication Flow**

   ```python
   async def authenticate_and_run(tool_context: ToolContext):
       try:
           # Request credentials
           auth_config = AuthConfig(type="oauth2", scopes=["read", "write"])
           tool_context.request_credential(auth_config)

           # Get and use credentials
           creds = tool_context.get_auth_response(auth_config)
           return await perform_authenticated_operation(creds)
       except ValueError as e:
           return {"error": f"Authentication failed: {str(e)}"}
   ```

3. **Memory and Artifact Integration**

   ```python
   async def process_with_resources(tool_context: ToolContext):
       # Search memory for context
       memory_results = tool_context.search_memory("relevant data")

       # List available artifacts
       artifacts = tool_context.list_artifacts()

       # Combine information
       return {
           "memory_context": memory_results,
           "available_artifacts": artifacts
       }
   ```

#### Integration Notes

- Extends CallbackContext for event handling
- Requires properly initialized services
- Manages function call identification
- Provides access to core ADK services

#### Service Dependencies

- **Memory Service**: Required for memory operations
- **Artifact Service**: Required for artifact management
- **Auth Handler**: Required for authentication flows
- **Event Actions**: Required for event management

### LongRunningFunctionTool (long_running_tool.py)

The `LongRunningFunctionTool` class extends `FunctionTool` to handle operations that may take a significant amount of time to complete. It provides asynchronous result handling for long-running operations within the ADK framework.

#### Class Definition

```python
class LongRunningFunctionTool(FunctionTool):
    is_long_running: bool = True  # Indicates this is a long-running operation
```

#### Core Features

1. **Asynchronous Operation**

   - Designed for time-intensive tasks
   - Returns results asynchronously
   - Maintains function call identification
   - Integrates with ADK's async framework

2. **Framework Integration**
   - Extends FunctionTool functionality
   - Preserves function signatures
   - Handles async result delivery
   - Manages operation state

#### Usage Example

```python
from google.adk.tools import LongRunningFunctionTool
import time

def process_large_dataset(data_path: str) -> dict:
    """Process a large dataset with potential long execution time.

    Args:
        data_path: Path to the dataset to process

    Returns:
        Dict containing processing results
    """
    # Simulate long-running operation
    time.sleep(10)  # In real use, this would be actual processing
    return {"status": "completed", "processed_items": 1000}

# Create a long-running tool
processing_tool = LongRunningFunctionTool(process_large_dataset)
```

#### Best Practices

1. **When to Use**

   - For operations taking more than a few seconds
   - CPU-intensive tasks
   - Network-bound operations
   - Batch processing jobs

2. **Implementation Guidelines**

   - Keep function signatures clean
   - Provide progress indicators when possible
   - Handle interruptions gracefully
   - Include proper error handling

3. **Resource Management**
   - Clean up resources on completion
   - Monitor memory usage
   - Implement timeout mechanisms
   - Handle cancellation requests

#### Common Patterns

1. **Progress Reporting**

   ```python
   def long_running_with_progress(task_id: str, tool_context: ToolContext) -> dict:
       total_steps = 100
       for step in range(total_steps):
           # Do work
           progress = (step + 1) / total_steps * 100
           # Report progress through appropriate channels
           time.sleep(0.1)  # Simulate work
       return {"task_id": task_id, "status": "complete"}

   progress_tool = LongRunningFunctionTool(long_running_with_progress)
   ```

2. **Resource Cleanup**

   ```python
   def managed_long_operation(resource_path: str) -> dict:
       try:
           # Acquire resources
           resource = acquire_resource(resource_path)

           # Perform long operation
           result = process_resource(resource)

           return {"status": "success", "result": result}
       finally:
           # Ensure cleanup happens
           cleanup_resource(resource)

   managed_tool = LongRunningFunctionTool(managed_long_operation)
   ```

3. **Error Handling**

   ```python
   def robust_long_operation(input_data: dict) -> dict:
       try:
           # Initialize state
           state = setup_operation(input_data)

           # Perform operation with checkpoints
           for chunk in process_in_chunks(state):
               try:
                   process_chunk(chunk)
               except ChunkError as e:
                   log_error(e)
                   continue

           return {"status": "complete", "errors": get_error_summary()}
       except Exception as e:
           return {"status": "failed", "error": str(e)}

   robust_tool = LongRunningFunctionTool(robust_long_operation)
   ```

#### Integration Notes

- **Framework Interaction**

  - Tool automatically marks itself as long-running
  - Results are delivered through async channels
  - Function call ID maintains operation context
  - Supports ADK's event system

- **Performance Considerations**

  - Monitor resource usage
  - Implement appropriate timeouts
  - Consider batch processing
  - Handle partial results

- **Error Handling**
  - Implement robust error recovery
  - Provide detailed error information
  - Consider retry mechanisms
  - Maintain operation state

#### Limitations and Considerations

1. **Resource Management**

   - Memory usage during long operations
   - Network connection stability
   - Timeout handling
   - State persistence

2. **Framework Integration**

   - Event system compatibility
   - Progress reporting mechanisms
   - Cancellation support
   - Result delivery guarantees

3. **Development Guidelines**
   - Test with various operation durations
   - Implement proper logging
   - Consider failure scenarios
   - Document timeout behaviors

### GoogleSearchTool (google_search_tool.py)

The `GoogleSearchTool` class is a specialized implementation of `BaseTool` that integrates with Gemini models to provide Google Search capabilities. It's unique in that it operates internally within the model and doesn't require local code execution.

#### Class Definition

```python
class GoogleSearchTool(BaseTool):
    """A built-in tool for Gemini models to access Google Search."""
```

#### Core Features

1. **Model Integration**

   - Built-in tool for Gemini models
   - Automatic search capability
   - Model-specific configuration
   - No local execution required

2. **Version Compatibility**
   - Supports Gemini 1.x (with restrictions)
   - Supports Gemini 2.x
   - Version-specific configurations
   - Automatic feature detection

#### Implementation Details

1. **Constructor**

   ```python
   def __init__(self):
       super().__init__(name='google_search', description='google_search')
   ```

   - Minimal initialization
   - Fixed tool identification
   - Internal model integration

2. **LLM Request Processing**
   ```python
   async def process_llm_request(self, *,
                               tool_context: ToolContext,
                               llm_request: LlmRequest) -> None
   ```
   - Configures search capabilities
   - Handles model version differences
   - Manages tool compatibility
   - Sets up search retrieval

#### Usage Example

```python
from google.adk.tools import google_search  # Pre-instantiated singleton

# The tool is automatically configured based on the model version
llm_request = LlmRequest(
    model="gemini-2.0",
    # ... other configuration ...
)

# The tool will be automatically integrated during request processing
await google_search.process_llm_request(
    tool_context=context,
    llm_request=llm_request
)
```

#### Version-Specific Behavior

1. **Gemini 1.x**

   ```python
   # Exclusive usage - cannot be combined with other tools
   llm_request.config.tools.append(
       types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())
   )
   ```

2. **Gemini 2.x**
   ```python
   # Can be combined with other tools
   llm_request.config.tools.append(
       types.Tool(google_search=types.GoogleSearch())
   )
   ```

#### Best Practices

1. **Model Selection**

   - Use appropriate model version
   - Consider compatibility requirements
   - Handle version-specific features
   - Plan for version transitions

2. **Tool Integration**

   - Use pre-instantiated singleton
   - Handle version restrictions
   - Consider tool combinations
   - Manage search context

3. **Error Handling**
   - Check model compatibility
   - Handle version mismatches
   - Manage tool conflicts
   - Provide fallback options

#### Limitations and Considerations

1. **Version Constraints**

   - Gemini 1.x: Exclusive tool usage
   - Gemini 2.x: Flexible integration
   - Model-specific features
   - Version migration paths

2. **Integration Requirements**

   - Model availability
   - API access setup
   - Version compatibility
   - Tool configuration

3. **Usage Guidelines**
   - Consider rate limits
   - Manage search context
   - Handle response formats
   - Plan for upgrades

#### Common Patterns

1. **Basic Integration**

   ```python
   from google.adk.tools import google_search
   from google.genai import types

   async def setup_search_request(model_version: str) -> None:
       request = LlmRequest(
           model=model_version,
           config=types.GenerateContentConfig()
       )
       await google_search.process_llm_request(
           tool_context=context,
           llm_request=request
       )
   ```

2. **Version Handling**

   ```python
   def configure_search_for_model(model: str) -> LlmRequest:
       request = LlmRequest(model=model)
       if model.startswith('gemini-1'):
           # Ensure no other tools are configured
           request.config.tools = []
       return request
   ```

3. **Error Management**
   ```python
   async def safe_search_setup(model: str) -> None:
       try:
           request = configure_search_for_model(model)
           await google_search.process_llm_request(
               tool_context=context,
               llm_request=request
           )
       except ValueError as e:
           # Handle incompatibility or configuration errors
           logger.error(f"Search setup failed: {e}")
           # Implement fallback strategy
   ```

#### Integration Notes

- **Automatic Configuration**

  - Tool self-configures based on model
  - Handles version-specific setup
  - Manages tool compatibility
  - Ensures proper integration

- **Model Requirements**

  - Requires Gemini model family
  - Version-specific features
  - API access configuration
  - Tool compatibility checks

- **Usage Context**
  - Internal model operation
  - No local execution needed
  - Automatic search integration
  - Response handling by model

---

_Note: This documentation is part of the ADK project. For detailed API references and examples, see individual tool documentation._
