# CrewAI Tool Deep Dive Documentation

## Architectural Overview

The `CrewaiTool` serves as a powerful bridge between CrewAI's collaborative agent framework and ADK's tool infrastructure. This adapter enables ADK agents to leverage CrewAI's extensive ecosystem of specialized tools, extending ADK capabilities into multi-agent collaboration and complex task orchestration.

### Core Architecture

```
┌────────────────────┐     ┌────────────────────┐
│                    │     │                    │
│   ADK Framework    │─────►  CrewaiTool        │
│                    │     │                    │
└────────────────────┘     └─────────┬──────────┘
                                     │
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │                     │
                           │  CrewAI Ecosystem   │
                           │                     │
                           └─────────┬───────────┘
                                     │
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │                     │
                           │  External Tools &   │
                           │  Services           │
                           │                     │
                           └─────────────────────┘
```

The `CrewaiTool` architecture consists of three main components:

1. **Adapter Layer**: Translates between ADK's tool interface and CrewAI's tool expectations
2. **Schema Conversion Layer**: Maps argument schemas between frameworks
3. **Execution Layer**: Handles the actual invocation of CrewAI tools

## Implementation Details

### Class Structure

The `CrewaiTool` class extends ADK's `FunctionTool` class, preserving all the fundamental capabilities while adding CrewAI-specific functionality:

```python
class CrewaiTool(FunctionTool):
  """Use this class to wrap a CrewAI tool.

  If the original tool name and description are not suitable, you can override
  them in the constructor.
  """

  tool: CrewaiBaseTool
  """The wrapped CrewAI tool."""

  def __init__(self, tool: CrewaiBaseTool, *, name: str, description: str):
    # Initialize with the CrewAI tool's run method
    super().__init__(tool.run)
    self.tool = tool

    # Handle name formatting (CrewAI allows spaces, ADK doesn't)
    if name:
      self.name = name
    elif tool.name:
      self.name = tool.name.replace(" ", "_").lower()

    # Handle description
    if description:
      self.description = description
    elif tool.description:
      self.description = tool.description
```

### Function Declaration Generation

The core mechanism that enables ADK to properly invoke CrewAI tools is the declaration conversion logic:

```python
@override
def _get_declaration(self) -> types.FunctionDeclaration:
  """Build the function declaration for the tool."""
  function_declaration = _automatic_function_calling_util.build_function_declaration_for_params_for_crewai(
      False,
      self.name,
      self.description,
      self.func,
      self.tool.args_schema.model_json_schema(),
  )
  return function_declaration
```

This method:

1. Extracts the CrewAI tool's schema
2. Converts it to a format compatible with ADK
3. Wraps it into a function declaration that ADK can properly interpret

## Under the Hood: Schema Translation

The `build_function_declaration_for_params_for_crewai` function handles the complex translation between CrewAI's Pydantic schemas and ADK's function declaration format.

Key translation challenges addressed:

1. **Type Mapping**: Converting CrewAI's Pydantic types to ADK-compatible types
2. **Metadata Preservation**: Retaining field descriptions and validations
3. **Schema Flattening**: Translating nested schemas appropriately
4. **Default Value Handling**: Ensuring default values are properly represented

## Integration Patterns

### 1. Direct Tool Integration

The simplest pattern - wrap a single CrewAI tool for immediate use:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from crewai.tools import SerperDevTool

# Create a CrewAI tool
search_tool = SerperDevTool()

# Wrap it for ADK use
adk_search_tool = CrewaiTool(
    tool=search_tool,
    name="web_search",
    description="Search the web for current information"
)

# Use in an ADK agent
agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[adk_search_tool],
    instructions="You help users find information online."
)
```

### 2. Tool Collection Integration

Adding multiple CrewAI tools to create a specialized agent:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from crewai.tools import (
    SerperDevTool,
    WebsiteSearchTool,
    FileReadTool,
    DirectoryReadTool
)

# Create CrewAI tools
search_tool = SerperDevTool()
website_tool = WebsiteSearchTool()
file_tool = FileReadTool()
directory_tool = DirectoryReadTool()

# Wrap all tools
adk_tools = [
    CrewaiTool(tool=search_tool, name="web_search", description="Search the web"),
    CrewaiTool(tool=website_tool, name="site_search", description="Search a specific website"),
    CrewaiTool(tool=file_tool, name="file_read", description="Read file contents"),
    CrewaiTool(tool=directory_tool, name="dir_read", description="List directory contents")
]

# Create a research agent with multiple tools
research_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=adk_tools,
    instructions="You are a research assistant that can search the web and local files."
)
```

### 3. Tool Customization Pattern

Creating specialized tools with custom parameters:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from crewai.tools import WebsiteSearchTool, PDFSearchTool

# Create tools with custom configurations
company_website_tool = WebsiteSearchTool(website_urls=["https://example.com"])
pdf_search_tool = PDFSearchTool(directory_path="./documents/")

# Wrap with descriptive names
adk_tools = [
    CrewaiTool(
        tool=company_website_tool,
        name="company_site_search",
        description="Search the company website for information"
    ),
    CrewaiTool(
        tool=pdf_search_tool,
        name="document_search",
        description="Search PDF documents in the documents directory"
    )
]

# Create an information retrieval agent
agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=adk_tools,
    instructions="You help retrieve information from company resources."
)
```

## Specialized CrewAI Tool Categories

CrewAI offers a rich ecosystem of tools that can be integrated into ADK through the `CrewaiTool` adapter:

### 1. Web Interaction Tools

| CrewAI Tool                  | Purpose                | Key Features                             |
| ---------------------------- | ---------------------- | ---------------------------------------- |
| `SerperDevTool`              | Web search             | Real-time internet search via Serper API |
| `WebsiteSearchTool`          | Website content search | RAG over specific websites               |
| `FirecrawlScrapeWebsiteTool` | Web scraping           | Extract content from websites            |
| `FirecrawlCrawlWebsiteTool`  | Web crawling           | Navigate and map website structure       |

### 2. File and Data Processing Tools

| CrewAI Tool         | Purpose           | Key Features             |
| ------------------- | ----------------- | ------------------------ |
| `FileReadTool`      | File reading      | Access file contents     |
| `FileWriteTool`     | File writing      | Save outputs to files    |
| `DirectoryReadTool` | Directory listing | Browse folder structures |
| `PDFSearchTool`     | PDF analysis      | RAG over PDF documents   |
| `CSVSearchTool`     | CSV data analysis | RAG over structured data |

### 3. Specialized Search and Retrieval Tools

| CrewAI Tool              | Purpose                        | Key Features                 |
| ------------------------ | ------------------------------ | ---------------------------- |
| `GithubSearchTool`       | Code search                    | Search GitHub repositories   |
| `YoutubeVideoSearchTool` | Video content search           | RAG over YouTube videos      |
| `EXASearchTool`          | Enhanced search                | Advanced search capabilities |
| `RagTool`                | Retrieval-augmented generation | General-purpose RAG          |

### 4. Creative and Multimodal Tools

| CrewAI Tool           | Purpose          | Key Features               |
| --------------------- | ---------------- | -------------------------- |
| `DALL-E Tool`         | Image generation | Create images from text    |
| `VisionTool`          | Image analysis   | Process and analyze images |
| `CodeInterpreterTool` | Code execution   | Run and analyze code       |

## Advanced Usage Scenarios

### 1. Multi-Modal Research Assistant

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool, FunctionTool
from crewai.tools import SerperDevTool, WebsiteSearchTool, VisionTool, FileWriteTool

# Create and wrap CrewAI tools
search_tool = CrewaiTool(tool=SerperDevTool(), name="web_search", description="Search the web")
website_tool = CrewaiTool(tool=WebsiteSearchTool(), name="website_search", description="Search specific websites")
vision_tool = CrewaiTool(tool=VisionTool(), name="analyze_image", description="Analyze image content")
save_tool = CrewaiTool(tool=FileWriteTool(), name="save_report", description="Save research report")

# Custom tool for analysis consolidation
def analyze_findings(search_results: str, visual_analysis: str) -> dict:
    """Analyze and combine text and visual research findings."""
    # Analysis logic here
    return {
        "combined_findings": f"Text: {search_results}\nVisual: {visual_analysis}",
        "confidence_score": 0.85
    }

# Create research agent with multi-modal capabilities
research_agent = LlmAgent(
    model="gemini-2.0-pro-vision",
    tools=[
        search_tool,
        website_tool,
        vision_tool,
        save_tool,
        FunctionTool(analyze_findings)
    ],
    instructions="""
    You are a multi-modal research assistant that can:
    1. Search the web for textual information
    2. Analyze image content for visual information
    3. Combine text and visual findings into comprehensive reports
    4. Save research outputs to files
    """
)
```

### 2. Code Analysis and Documentation System

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from crewai.tools import (
    GithubSearchTool,
    DirectoryReadTool,
    CodeDocsSearchTool,
    FileWriteTool
)

# Create a suite of code analysis tools
github_tool = CrewaiTool(
    tool=GithubSearchTool(),
    name="github_search",
    description="Search GitHub repositories for code examples"
)
directory_tool = CrewaiTool(
    tool=DirectoryReadTool(directory="./src/"),
    name="project_code_browse",
    description="Browse project source code"
)
docs_tool = CrewaiTool(
    tool=CodeDocsSearchTool(),
    name="code_docs_search",
    description="Search code documentation"
)
save_tool = CrewaiTool(
    tool=FileWriteTool(),
    name="save_documentation",
    description="Save generated documentation"
)

# Create code documentation agent
code_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[github_tool, directory_tool, docs_tool, save_tool],
    instructions="""
    You are a code documentation specialist that can:
    1. Analyze project source code
    2. Search GitHub for similar implementations
    3. Review existing documentation
    4. Generate comprehensive, well-structured documentation
    """
)
```

### 3. RAG-Enhanced Knowledge Base System

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from crewai.tools import (
    RagTool,
    PDFSearchTool,
    WebsiteSearchTool,
    FileWriteTool
)

# Configure knowledge sources
internal_docs = CrewaiTool(
    tool=PDFSearchTool(directory_path="./knowledge_base/"),
    name="internal_knowledge",
    description="Search internal PDF documentation"
)
public_docs = CrewaiTool(
    tool=WebsiteSearchTool(website_urls=["https://docs.example.com"]),
    name="public_knowledge",
    description="Search public documentation website"
)
general_rag = CrewaiTool(
    tool=RagTool(sources=["./wiki", "./manuals"]),
    name="general_knowledge",
    description="Search general knowledge base"
)
save_answer = CrewaiTool(
    tool=FileWriteTool(),
    name="save_answer",
    description="Save the answer to a file"
)

# Create knowledge base agent
kb_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[internal_docs, public_docs, general_rag, save_answer],
    instructions="""
    You are a knowledge base assistant that can:
    1. Search internal documentation
    2. Reference public documentation
    3. Access general knowledge sources
    4. Provide comprehensive answers with citations
    """
)
```

## Performance Considerations

### Optimization Strategies

1. **CrewAI Tool Caching**

CrewAI tools support caching for improved performance. When integrated with ADK, this caching mechanism remains functional:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from crewai.tools import SerperDevTool

# Create cached search tool
search_tool = SerperDevTool()

# Define custom caching logic
def cache_search_results(args, result):
    # Only cache successful searches with substantial results
    if result and len(result) > 100:
        return True
    return False

# Assign caching logic
search_tool.cache_function = cache_search_results

# Wrap for ADK
adk_search = CrewaiTool(
    tool=search_tool,
    name="web_search",
    description="Search the web for current information"
)

# Use in agent
agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[adk_search],
    instructions="You help users find information online."
)
```

2. **Selective Tool Loading**

Load only necessary tools to minimize overhead:

```python
# Import tools individually instead of entire collections
from crewai.tools import SerperDevTool, WebsiteSearchTool

# Avoid importing unused tools
# from crewai.tools import *  # Not recommended
```

3. **Parameter Tuning**

Configure CrewAI tools with optimized parameters before wrapping:

```python
from crewai.tools import WebsiteSearchTool

# Create tool with optimized parameters
optimized_website_tool = WebsiteSearchTool(
    website_urls=["https://example.com"],
    max_results=5,  # Limit results for faster processing
    chunk_size=500  # Optimize chunk size for Gemini models
)
```

## Error Handling and Debugging

### Common Issues and Solutions

| Issue                    | Common Cause             | Solution                               |
| ------------------------ | ------------------------ | -------------------------------------- |
| ImportError              | Python version < 3.10    | Upgrade Python to 3.10+                |
| Missing dependencies     | Extensions not installed | `pip install 'google-adk[extensions]'` |
| Schema conversion errors | Complex CrewAI schemas   | Use simpler parameter schemas          |
| Runtime errors           | API key configuration    | Ensure all required API keys are set   |
| Execution timeout        | Network calls in tools   | Implement timeouts and retries         |

### Debugging Techniques

1. **Enable Verbose Mode**

```python
from crewai.tools import SerperDevTool
from google.adk.tools import CrewaiTool

# Create tools with verbose logging
search_tool = SerperDevTool(verbose=True)
adk_search = CrewaiTool(
    tool=search_tool,
    name="web_search",
    description="Search the web"
)
```

2. **Isolated Tool Testing**

```python
from crewai.tools import SerperDevTool

# Test CrewAI tool directly before wrapping
search_tool = SerperDevTool()
raw_result = search_tool.run(query="test query")
print(f"Raw CrewAI result: {raw_result}")

# Then test wrapped tool
from google.adk.tools import CrewaiTool
adk_search = CrewaiTool(
    tool=search_tool,
    name="web_search",
    description="Search the web"
)
wrapped_result = adk_search._run(query="test query")
print(f"Wrapped ADK result: {wrapped_result}")
```

## Integration with Other ADK Components

### 1. Combining with Native ADK Tools

```python
from google.adk.agents import LlmAgent
from google.adk.tools import (
    CrewaiTool,
    google_search_tool,
    load_memory_tool
)
from crewai.tools import WebsiteSearchTool

# Mix CrewAI and native ADK tools
tools = [
    # CrewAI tool
    CrewaiTool(
        tool=WebsiteSearchTool(),
        name="website_search",
        description="Search specific websites"
    ),
    # Native ADK tools
    google_search_tool,
    load_memory_tool
]

# Create agent with hybrid tools
agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=tools,
    instructions="You can search the web, specific websites, and recall past conversations."
)
```

### 2. Integration with ADK Memory System

```python
from google.adk.agents import LlmAgent
from google.adk.tools import (
    CrewaiTool,
    load_memory_tool,
    preload_memory_tool
)
from crewai.tools import SerperDevTool

# Create a memory-aware agent with CrewAI search
agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        # CrewAI tool for search
        CrewaiTool(
            tool=SerperDevTool(),
            name="web_search",
            description="Search the web for information"
        ),
        # ADK memory tools
        load_memory_tool,
        preload_memory_tool
    ],
    instructions="""
    You are an assistant that can:
    1. Search the web for current information
    2. Remember past conversations
    3. Provide contextually relevant answers
    """
)
```

### 3. Integration with ADK Session Context

```python
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from google.adk.sessions import Session
from crewai.tools import WebsiteSearchTool

# Create session-aware website search
def create_website_search_agent(session: Session):
    # Get user's preferred websites from session
    user_preferences = session.get_user_preferences()
    preferred_sites = user_preferences.get("preferred_websites", ["https://example.com"])

    # Create tool with user preferences
    website_tool = WebsiteSearchTool(website_urls=preferred_sites)

    # Wrap for ADK
    adk_website_search = CrewaiTool(
        tool=website_tool,
        name="preferred_site_search",
        description="Search your preferred websites"
    )

    return LlmAgent(
        model="gemini-2.0-flash",
        tools=[adk_website_search],
        instructions=f"You can search the user's preferred websites: {', '.join(preferred_sites)}"
    )
```

## Security Considerations

### 1. API Key Management

CrewAI tools often require external API keys. Secure these properly:

```python
import os
from google.adk.agents import LlmAgent
from google.adk.tools import CrewaiTool
from crewai.tools import SerperDevTool

# Securely load API keys from environment
os.environ["SERPER_API_KEY"] = "***"  # Set this securely in production

# Create tool with API key from environment
search_tool = SerperDevTool()  # Automatically uses SERPER_API_KEY from env

# Wrap for ADK
adk_search = CrewaiTool(
    tool=search_tool,
    name="web_search",
    description="Search the web"
)
```

### 2. Tool Permission Scoping

Limit tool capabilities to minimum required permissions:

```python
from crewai.tools import FileReadTool, WebsiteSearchTool

# Scope file access to specific directory
file_tool = FileReadTool(allowed_paths=["./public_docs/"])

# Limit website search to specific domains
website_tool = WebsiteSearchTool(website_urls=["https://docs.example.com"])
```

### 3. Input Validation

Ensure proper validation for all tool inputs:

```python
from pydantic import BaseModel, Field, validator
from crewai.tools import BaseTool

# Create a secure tool with validated inputs
class SecureSearchInput(BaseModel):
    query: str = Field(..., description="Search query")

    @validator("query")
    def sanitize_query(cls, value):
        # Simple sanitization example
        disallowed = ["--", ";", "DROP", "DELETE", "UPDATE"]
        for term in disallowed:
            if term.lower() in value.lower():
                raise ValueError(f"Query contains disallowed term: {term}")
        return value

class SecureSearchTool(BaseTool):
    name = "secure_search"
    description = "Search the web securely"
    args_schema = SecureSearchInput

    def _run(self, query: str):
        # Tool implementation
        return f"Secure search results for: {query}"
```

## Future Considerations

### 1. CrewAI System Evolution

As CrewAI continues to evolve, the `CrewaiTool` adapter will need updates to maintain compatibility. Key areas to watch:

- **Tool Schema Changes**: Updates to CrewAI's tool schema definition system
- **New Tool Categories**: Integration of new specialized tool types
- **Performance Optimizations**: Keeping pace with CrewAI's performance improvements

### 2. Advanced Integration Patterns

Future development directions may include:

- **Bi-directional Integration**: Enabling ADK tools to be used within CrewAI systems
- **Crew Orchestration**: Supporting CrewAI's multi-agent coordination within ADK
- **Hybrid Tool Chains**: Building composite tools that leverage both frameworks

### 3. Enterprise Applications

As enterprise adoption grows, additional considerations may include:

- **Compliance Tools**: Integration with audit and compliance systems
- **Enterprise Authentication**: Support for enterprise SSO and auth systems
- **Observability**: Enhanced logging and monitoring capabilities

## Conclusion

The `CrewaiTool` adapter serves as a powerful bridge between ADK and the CrewAI ecosystem, enabling ADK agents to leverage a wide range of specialized tools. By following the integration patterns and best practices outlined in this documentation, developers can significantly enhance their ADK agents with capabilities ranging from web search and file manipulation to advanced RAG implementation and multi-modal processing.

This integration demonstrates the extensibility of the ADK framework, allowing it to incorporate the strengths of complementary AI agent frameworks while maintaining its core architecture and development philosophy.
