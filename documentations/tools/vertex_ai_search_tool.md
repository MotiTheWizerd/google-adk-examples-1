# Vertex AI Search Tool Documentation

## Overview

The `VertexAiSearchTool` is a built-in tool that integrates Vertex AI Search capabilities into ADK agents. It enables agents to perform semantic searches over data stored in Vertex AI Search data stores or search engines.

## Class Definition

```python
class VertexAiSearchTool(BaseTool):
    def __init__(self, *, data_store_id: Optional[str] = None, search_engine_id: Optional[str] = None):
        # ...
```

## Key Features

- Direct integration with Vertex AI Search
- Support for both data store and search engine modes
- Automatic configuration for Gemini models
- Built-in validation for model compatibility

## Usage

### Initialization

You must provide either a `data_store_id` OR a `search_engine_id` (not both):

```python
# Using data store
search_tool = VertexAiSearchTool(
    data_store_id="projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore}"
)

# Using search engine
search_tool = VertexAiSearchTool(
    search_engine_id="projects/{project}/locations/{location}/collections/{collection}/engines/{engine}"
)
```

### Integration with Agents

```python
from google.adk.tools import VertexAiSearchTool
from google.adk.agents import Agent

agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    tools=[VertexAiSearchTool(data_store_id="your-data-store-id")]
)
```

## Model Compatibility

- **Gemini 1.x**:
  - Cannot be used with other tools
  - Uses dedicated Vertex AI Search integration
- **Other Models**:
  - Not currently supported
  - Will raise a ValueError if attempted

## Resource IDs Format

### Data Store ID Format

```
projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore}
```

### Search Engine ID Format

```
projects/{project}/locations/{location}/collections/{collection}/engines/{engine}
```

## Error Handling

The tool includes validation for:

- Mutually exclusive data_store_id and search_engine_id
- Model compatibility checks
- Resource ID format validation

## Best Practices

1. **Resource Selection**:

   - Choose between data store or search engine based on your use case
   - Use data stores for simpler search needs
   - Use search engines for more advanced search capabilities

2. **Model Selection**:

   - Use with Gemini 1.x models for optimal compatibility
   - Be aware of tool combination limitations

3. **Error Handling**:
   - Always handle potential ValueError exceptions
   - Validate resource IDs before initialization

## Related Components

- Works closely with the Vertex AI Search service
- Integrates with ADK's agent system
- Compatible with Gemini model family

## Example

```python
from google.adk.tools import VertexAiSearchTool
from google.adk.agents import Agent

# Initialize the search tool
search_tool = VertexAiSearchTool(
    data_store_id="projects/my-project/locations/us-central1/collections/my-collection/dataStores/my-datastore"
)

# Create an agent with the search tool
agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    tools=[search_tool]
)

# The agent can now use Vertex AI Search capabilities
response = agent.run("Search for relevant information about machine learning")
```

## Limitations

1. Cannot be used with other tools in Gemini 1.x
2. Only supports Gemini model family
3. Requires either data_store_id or search_engine_id (mutually exclusive)

## See Also

- [Vertex AI Search Documentation](https://cloud.google.com/vertex-ai/docs/search)
- [Gemini Model Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
