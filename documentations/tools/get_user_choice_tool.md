# Get User Choice Tool Documentation

## Overview

The `get_user_choice_tool` is a specialized long-running tool that facilitates interactive decision-making by presenting options to users and collecting their choices. It extends `LongRunningFunctionTool` to handle asynchronous user interactions properly.

## Function Definition

```python
def get_user_choice(
    options: list[str],
    tool_context: ToolContext
) -> Optional[str]:
    """Provides the options to the user and asks them to choose one."""
    tool_context.actions.skip_summarization = True
    return None
```

## Key Features

- Interactive user choice collection
- Long-running operation support
- Summarization control
- Type-safe option handling
- Asynchronous interaction flow

## Usage

### Basic Integration

```python
from google.adk.tools import get_user_choice_tool
from google.adk.agents import Agent

# Create an agent with user choice capability
agent = Agent(
    name="decision_maker",
    description="Helps users make decisions",
    model="gemini-2.0-flash",
    tools=[get_user_choice_tool]
)

# Example usage in agent prompt
"""
Please help the user choose a color:
1. Present these options: ["red", "blue", "green"]
2. Get their choice using get_user_choice_tool
3. Proceed based on their selection
"""
```

### Handling User Choices

```python
from google.adk.tools import get_user_choice_tool
from google.adk.agents import Agent

async def handle_user_preferences():
    agent = Agent(
        name="preference_handler",
        description="Handles user preferences",
        model="gemini-2.0-flash",
        tools=[get_user_choice_tool]
    )

    # Define options
    color_options = ["Red", "Blue", "Green", "Yellow"]

    # Get user choice through agent
    response = await agent.run(
        f"Please ask the user to choose their preferred color "
        f"from these options: {color_options}. "
        f"Use get_user_choice to collect their selection."
    )

    return response
```

## Technical Details

### Tool Context Integration

The tool:

1. Accepts a list of options and tool context
2. Disables summarization for the interaction
3. Handles the choice collection asynchronously
4. Returns the selected option or None

### Long-Running Operation

- Inherits from LongRunningFunctionTool
- Manages asynchronous user interaction
- Maintains context during the operation
- Handles interruptions gracefully

## Best Practices

1. **Option Presentation**:

   - Keep options clear and concise
   - Use consistent formatting
   - Limit number of choices (5-7 max)
   - Provide descriptive labels

2. **Error Handling**:

   - Handle None returns
   - Validate option list
   - Provide fallback options
   - Consider timeout scenarios

3. **User Experience**:
   - Clear instructions
   - Reasonable timeouts
   - Confirmation messages
   - Error feedback

## Example: Complex Integration

```python
from google.adk.tools import get_user_choice_tool
from google.adk.agents import Agent
from typing import List, Optional, Dict

class InteractiveDecisionMaker:
    def __init__(self):
        self.agent = Agent(
            name="interactive_assistant",
            description="Assists with complex decision making",
            model="gemini-2.0-flash",
            tools=[get_user_choice_tool]
        )
        self.choices_history: List[str] = []

    async def get_user_preference(
        self,
        category: str,
        options: List[str],
        description: str = ""
    ) -> Optional[str]:
        # Format the prompt
        prompt = (
            f"Category: {category}\n"
            f"Description: {description}\n"
            f"Please help the user choose from these options: {options}\n"
            "1. Present the options clearly\n"
            "2. Use get_user_choice to collect their selection\n"
            "3. Acknowledge their choice\n"
        )

        try:
            response = await self.agent.run(prompt)

            if response:
                self.choices_history.append(response)

            return response

        except Exception as e:
            print(f"Error during choice collection: {e}")
            return None

# Usage example
async def main():
    decision_maker = InteractiveDecisionMaker()

    # Define choice categories
    categories = {
        "color": {
            "options": ["Red", "Blue", "Green"],
            "description": "Choose your preferred color theme"
        },
        "size": {
            "options": ["Small", "Medium", "Large"],
            "description": "Select your preferred size"
        }
    }

    # Collect user preferences
    preferences: Dict[str, str] = {}

    for category, details in categories.items():
        choice = await decision_maker.get_user_preference(
            category=category,
            options=details["options"],
            description=details["description"]
        )

        if choice:
            preferences[category] = choice

    return preferences
```

## Limitations

1. No built-in validation
2. Single choice only (no multi-select)
3. No option grouping
4. No direct choice persistence

## Related Components

- Extends LongRunningFunctionTool
- Requires ToolContext
- Works with ADK's agent framework
- Compatible with all ADK models

## See Also

- [Long Running Tool Documentation](long_running_tool.md)
- [Tool Context Documentation](tool_context.md)
- [Agent Framework Documentation](../agents/index.md)
