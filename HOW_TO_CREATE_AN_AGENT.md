# How to Create a New Agent (Boilerplate Guide)

This guide provides a boilerplate and step-by-step instructions for creating a new basic agent in this project.

## Overview

The general structure involves:

1.  A dedicated directory for the agent within `agents/`.
2.  A Python file for the agent's logic within its directory.
3.  A corresponding prompt file within `prompts/`.
4.  A factory function (`get_<agent_name>`) that instantiates and returns the configured `LlmAgent`.

## Steps

### 1. Create the Agent's Directory

- Navigate to the `agents/` directory in your project.
- Create a new folder for your agent. For example, if your agent is named `example_agent`, create the directory:
  ```bash
  agents/example_agent/
  ```

### 2. Create the Agent's Python File & `__init__.py`

- Inside the new agent directory (e.g., `agents/example_agent/`), create two files:
  1.  `__init__.py` (this file can be empty; it helps Python recognize the directory as a package).
  2.  A Python file named after your agent, e.g., `example_agent.py`.

### 3. Create the Prompt File

- Navigate to the `prompts/` directory.
- Create a Python file for your agent's prompt, e.g., `example_agent_prompt.py`.
- Inside this file, define a string variable for your prompt.

**Boilerplate for `prompts/example_agent_prompt.py`:**

```python
# prompts/example_agent_prompt.py

example_agent_prompt = \"\"\"
You are 'Example Agent'.
Your primary function is to [clearly define the agent's main goal or task].

Instructions:
1. Receive input [describe expected input].
2. Perform [describe core logic/steps].
3. Return the output in [describe desired output format, e.g., "a concise summary", "a JSON object with keys 'x', 'y'"].

Example:
Input: [Provide a simple input example]
Output: [Provide a corresponding output example]
\"\"\"
```

\_
```

### 4. Implement the Agent Factory Function

- Open your agent's Python file (e.g., `agents/example_agent/example_agent.py`).
- Implement the factory function.

**Boilerplate for `agents/example_agent/example_agent.py`:**

```python
# agents/example_agent/example_agent.py

from google.adk.agents import BaseAgent, LlmAgent
from typing import List

# Import the prompt
# Option 1: If using a simple string prompt
from prompts.example_agent_prompt import example_agent_prompt
# Option 2: If using a dictionary-based prompt
# from prompts.example_agent_prompt import example_agent_prompt_config

# Import any tools your agent might need (optional)
# from tools.your_specific_tool import your_specific_tool

def get_example_agent(sub_agents: List[BaseAgent] = []) -> LlmAgent:
    \"\"\"
    Factory function to create and configure the ExampleAgent.

    This agent serves as a boilerplate for creating new agents.
    It takes a simple input and returns a processed output.
    \"\"\"

    # If using Option 1 (string prompt):
    agent_instruction = example_agent_prompt
    agent_name = "ExampleAgent"
    agent_description = "A boilerplate agent that demonstrates basic functionality."

    # If using Option 2 (dictionary prompt):
    # agent_instruction = example_agent_prompt_config["instruction"]
    # agent_name = example_agent_prompt_config["name"]
    # agent_description = example_agent_prompt_config["description"]

    example_agent_instance = LlmAgent(
        name=agent_name,
        description=agent_description,
        instruction=agent_instruction,
        model="gemini-1.5-flash-latest", # Or your preferred model
        sub_agents=sub_agents,
        tools=[
            # your_specific_tool, # Add any tools here if needed
        ],
        # output_key="example_output" # Optional: specify if you want the agent's output nested under this key
    )
    return example_agent_instance

# Example of how you might test this agent (optional, usually done in a separate test file or main script)
if __name__ == '__main__':
    agent = get_example_agent()
    # This is a conceptual test; actual invocation depends on your ADK setup
    # result = agent.execute(request="Sample input for example agent")
    # print(f"Agent Result: {result}")
    print(f"Agent '{agent.name}' created successfully with description: '{agent.description}'")
    print(f"Instruction: {agent.instruction}")
```

### 5. Register and Use the Agent

- To use your new agent, you'll need to import its factory function into the relevant part of your application (e.g., your main script, an orchestrator agent, or a specific workflow file).
- Call the factory function to get an instance of the agent.

**Conceptual Example (in `your_main_script.py` or similar):**

```python
# from agents.example_agent.example_agent import get_example_agent
# from agents.another_agent.another_agent import get_another_agent

# ... your existing setup ...

# example_agent_instance = get_example_agent()
# another_agent_instance = get_another_agent(sub_agents=[example_agent_instance])

# Now you can use example_agent_instance or another_agent_instance as part of your agent sequence or logic.
# For example, if you have a TeamManager or a sequential execution flow:
# team_manager.add_delegate(example_agent_instance)
# result = sequential_flow.execute(initial_input, agents=[example_agent_instance, ...])
```

## Summary

This boilerplate provides a starting point. You will need to:

- Tailor the prompt in `prompts/example_agent_prompt.py` to your agent's specific task.
- Update the `name`, `description`, and potentially `model`, `tools`, or `output_key` in `agents/example_agent/example_agent.py`.
- Add any specific logic or tool integrations required by your agent.
- Write unit tests for your new agent's functionality, especially if it includes custom logic or uses tools.

Remember to follow the project's coding standards, including type hints and docstrings.
