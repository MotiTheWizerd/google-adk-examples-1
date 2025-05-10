# Exit Loop Tool Documentation

## Overview

The `exit_loop_tool.py` provides a simple but crucial function for controlling agent execution flow. It allows an agent to gracefully exit from a loop or recursive operation by setting an escalation flag in the tool context.

## Function Definition

```python
def exit_loop(tool_context: ToolContext):
    """Exits the loop.

    Call this function only when you are instructed to do so.
    """
    tool_context.actions.escalate = True
```

## Key Features

- Simple, focused functionality
- Direct tool context manipulation
- Clean loop termination
- Non-disruptive execution flow control

## Usage

### Basic Integration

```python
from google.adk.tools import exit_loop
from google.adk.tools import FunctionTool
from google.adk.agents import Agent

# Create the exit loop tool
exit_tool = FunctionTool(
    function=exit_loop,
    name="exit_loop",
    description="Exits the current loop when instructed"
)

# Use in an agent
agent = Agent(
    name="loop_controller",
    description="Agent that can control loop execution",
    model="gemini-2.0-flash",
    tools=[exit_tool]
)
```

### Loop Control Example

```python
from google.adk.tools import exit_loop, FunctionTool
from google.adk.agents import Agent

# Create a loop-aware agent
async def run_controlled_loop():
    agent = Agent(
        name="task_processor",
        description="Processes tasks with loop control",
        model="gemini-2.0-flash",
        tools=[
            FunctionTool(
                function=exit_loop,
                name="exit_loop",
                description="Exit the loop when all tasks are complete"
            )
        ]
    )

    tasks = ["task1", "task2", "task3"]

    while tasks:
        current_task = tasks.pop(0)
        response = await agent.run(
            f"Process {current_task}. "
            "Use exit_loop if this was the last task."
        )

        if agent.tool_context.actions.escalate:
            break
```

## Technical Details

### Tool Context Integration

The tool works by:

1. Accepting a ToolContext parameter
2. Setting the escalate flag to True
3. Allowing the agent framework to handle the loop exit

### Execution Flow

When called, the tool:

1. Sets `tool_context.actions.escalate = True`
2. Returns control to the agent framework
3. Framework detects escalation flag
4. Loop or recursive operation is terminated

## Best Practices

1. **Usage Guidelines**:

   - Only use when explicitly needed
   - Provide clear instructions for exit conditions
   - Verify loop termination requirements
   - Handle post-exit cleanup if necessary

2. **Integration**:

   - Include clear tool description
   - Document exit conditions
   - Handle escalation state appropriately
   - Clean up resources after exit

3. **Error Prevention**:
   - Validate exit conditions
   - Include safety checks
   - Handle edge cases
   - Maintain state consistency

## Example: Complex Integration

```python
from google.adk.tools import exit_loop, FunctionTool
from google.adk.agents import Agent
from typing import List, Optional

class TaskProcessor:
    def __init__(self):
        self.agent = Agent(
            name="advanced_processor",
            description="Processes tasks with sophisticated loop control",
            model="gemini-2.0-flash",
            tools=[
                FunctionTool(
                    function=exit_loop,
                    name="exit_loop",
                    description=(
                        "Exit the processing loop when either all tasks "
                        "are complete or an error condition is met"
                    )
                )
            ]
        )
        self.tasks: List[str] = []
        self.results: List[str] = []
        self.error: Optional[str] = None

    async def process_tasks(self, tasks: List[str]) -> List[str]:
        self.tasks = tasks.copy()
        self.results = []

        while self.tasks:
            try:
                current_task = self.tasks[0]

                # Process task with agent
                response = await self.agent.run(
                    f"Process task: {current_task}\n"
                    "Instructions:\n"
                    "1. Process the task normally\n"
                    "2. Use exit_loop if:\n"
                    "   - This was the last task\n"
                    "   - An error occurred\n"
                    "   - Processing should stop\n"
                )

                # Check for loop exit
                if self.agent.tool_context.actions.escalate:
                    if self.error:
                        break

                # Task completed successfully
                self.results.append(response)
                self.tasks.pop(0)

            except Exception as e:
                self.error = str(e)
                break

        return self.results

# Usage example
async def main():
    processor = TaskProcessor()
    tasks = [
        "Analyze data",
        "Generate report",
        "Send notifications"
    ]

    results = await processor.process_tasks(tasks)

    if processor.error:
        print(f"Processing stopped due to error: {processor.error}")
    else:
        print(f"Completed tasks: {len(results)}")
```

## Limitations

1. Only affects the immediate loop context
2. Requires proper tool context setup
3. No built-in condition checking
4. Cannot specify exit reason directly

## Related Components

- Requires ToolContext
- Works with ADK's agent framework
- Compatible with all ADK models
- Integrates with FunctionTool

## See Also

- [Tool Context Documentation](tool_context.md)
- [Function Tool Documentation](function_tool.md)
- [Agent Framework Documentation](../agents/index.md)
