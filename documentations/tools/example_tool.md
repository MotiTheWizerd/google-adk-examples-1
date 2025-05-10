# Example Tool Documentation

## Overview

The `ExampleTool` is a specialized tool that enhances LLM requests by adding few-shot examples. It's designed to improve model performance by providing relevant examples before the actual task, implementing few-shot learning capabilities in the ADK framework.

## Class Definition

```python
class ExampleTool(BaseTool):
    def __init__(self, examples: Union[list[Example], BaseExampleProvider]):
        super().__init__(name='example_tool', description='example tool')
        self.examples = (
            TypeAdapter(list[Example]).validate_python(examples)
            if isinstance(examples, list)
            else examples
        )
```

## Key Features

- Adds few-shot examples to LLM requests
- Supports both static example lists and dynamic providers
- Automatic example validation
- Model-specific example formatting
- Seamless integration with ADK's LLM request pipeline

## Usage

### Basic Integration

```python
from google.adk.tools import ExampleTool
from google.adk.examples import Example
from google.adk.agents import Agent

# Create examples
examples = [
    Example(
        input="Translate 'hello' to French",
        output="'hello' in French is 'bonjour'"
    ),
    Example(
        input="Translate 'goodbye' to French",
        output="'goodbye' in French is 'au revoir'"
    )
]

# Create the example tool
example_tool = ExampleTool(examples=examples)

# Use in an agent
translation_agent = Agent(
    name="translator",
    description="Translates text to French",
    model="gemini-2.0-flash",
    tools=[example_tool]
)
```

### Using Example Providers

```python
from google.adk.examples import BaseExampleProvider

class DynamicTranslationExamples(BaseExampleProvider):
    def get_examples(self, input_text: str) -> list[Example]:
        # Dynamically generate relevant examples
        return [
            Example(
                input=f"Similar translation task: {input_text}",
                output="Corresponding translation result"
            )
        ]

# Create tool with dynamic provider
dynamic_example_tool = ExampleTool(
    examples=DynamicTranslationExamples()
)
```

## Technical Details

### Example Processing

1. The tool checks for user content in the tool context
2. If valid content is found, it processes the examples
3. Examples are formatted according to the model's requirements
4. Formatted examples are appended to the LLM request

### Example Validation

- List examples are validated using Pydantic's TypeAdapter
- Provider examples are validated when retrieved
- Examples must conform to the Example class structure

### LLM Request Integration

The tool modifies the LLM request by:

1. Accessing the user's input text
2. Building example-specific instructions
3. Appending the instructions to the request
4. Preserving the original request structure

## Best Practices

1. **Example Selection**:

   - Choose relevant examples for the task
   - Keep examples concise and clear
   - Use a consistent format across examples
   - Include diverse but related cases

2. **Provider Implementation**:

   - Make providers task-specific
   - Implement efficient example generation
   - Cache frequently used examples
   - Handle edge cases gracefully

3. **Performance Optimization**:
   - Limit the number of examples (2-5 typically sufficient)
   - Prioritize quality over quantity
   - Consider example relevance to input
   - Monitor impact on response time

## Example: Complex Integration

```python
from google.adk.tools import ExampleTool
from google.adk.examples import Example, BaseExampleProvider
from google.adk.agents import Agent
from typing import List

# Create a sophisticated example provider
class ContextAwareExamples(BaseExampleProvider):
    def __init__(self):
        self.example_cache = {}

    def get_examples(self, input_text: str) -> List[Example]:
        # Check cache
        if input_text in self.example_cache:
            return self.example_cache[input_text]

        # Generate contextual examples
        examples = self._generate_relevant_examples(input_text)

        # Cache for future use
        self.example_cache[input_text] = examples
        return examples

    def _generate_relevant_examples(self, input_text: str) -> List[Example]:
        # Implementation of context-aware example generation
        pass

# Create static fallback examples
fallback_examples = [
    Example(
        input="Default example input",
        output="Default example output"
    )
]

# Combine both approaches
class HybridExampleProvider(BaseExampleProvider):
    def __init__(self):
        self.dynamic_provider = ContextAwareExamples()
        self.fallback_examples = fallback_examples

    def get_examples(self, input_text: str) -> List[Example]:
        try:
            return self.dynamic_provider.get_examples(input_text)
        except Exception:
            return self.fallback_examples

# Create and use the tool
example_tool = ExampleTool(
    examples=HybridExampleProvider()
)

# Create an agent with the example tool
agent = Agent(
    name="smart_agent",
    description="Uses context-aware examples",
    model="gemini-2.0-flash",
    tools=[example_tool]
)

# Use the agent
response = await agent.run(
    "Process this with relevant examples"
)
```

## Limitations

1. Examples must match the Example class structure
2. Tool name and description are fixed
3. Requires valid user content in tool context
4. Example processing may impact request latency

## Related Components

- Extends ADK's BaseTool
- Integrates with Example and BaseExampleProvider
- Works with ADK's LLM request pipeline
- Compatible with all ADK models

## See Also

- [Example Class Documentation](../examples/example.md)
- [BaseExampleProvider Documentation](../examples/base_example_provider.md)
- [LLM Request Documentation](../models/llm_request.md)
