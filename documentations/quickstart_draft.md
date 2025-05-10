# ADK Quickstart Guide (Draft)

## 1. Installation

### Stable Release (Recommended)

Install the latest stable version from PyPI:

```bash
pip install google-adk
```

### Development Version (Bleeding Edge)

Install directly from the main branch on GitHub:

```bash
pip install git+https://github.com/google/adk-python.git@main
```

_Note: The dev version may include experimental changes or bugs._

---

## 2. Minimal Agent Example

### Single Agent

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash",  # Or your preferred Gemini model
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
```

### Multi-Agent System

```python
from google.adk.agents import LlmAgent

# Define individual agents
greeter = LlmAgent(name="greeter", model="gemini-2.0-flash", ...)
task_executor = LlmAgent(name="task_executor", model="gemini-2.0-flash", ...)

# Create parent agent and assign children via sub_agents
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and tasks.",
    sub_agents=[
        greeter,
        task_executor
    ]
)
```

---

## 3. Running an Agent

### CLI

Run an agent interactively from the command line:

```bash
adk run path/to/your_agent
```

### Web UI

Launch the development web UI:

```bash
adk web path/to/your_agent
```

### API Server

Start an API server for your agent:

```bash
adk api_server path/to/your_agent
```

---

## 4. Next Steps

- Explore the full documentation: https://google.github.io/adk-docs
- Try out more advanced features (multi-agent, custom tools, evaluation, deployment)
- Check out the `examples/` directory for more sample agents

---
