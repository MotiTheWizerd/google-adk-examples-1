# ADK Documentation Plan

## 1. Overview

- **Project Name:** Agent Development Kit (ADK)
- **Purpose:** Python toolkit for building, evaluating, and deploying AI agents. Modular, model-agnostic, and designed for both simple and complex workflows.
- **Audience:** Python developers building agent-based systems, especially those integrating with Google's stack.

## 2. Quickstart

- Installation instructions (pip, dev version)
- Minimal agent example (single agent, multi-agent)
- Running an agent (CLI, web UI, API server)

## 3. Project Structure

- Directory/module overview:
  - `agents/`: Agent classes and orchestration
  - `tools/`: Built-in and extensible tools
  - `flows/`: Workflow and orchestration logic
  - `models/`: LLM and model connection logic
  - `memory/`: Memory backends
  - `sessions/`: Session and state management
  - `evaluation/`: Agent and response evaluation
  - `code_executors/`: Code execution backends
  - `artifacts/`: Artifact management
  - `events/`: Event handling
  - `auth/`: Authentication
  - `cli/`: Command-line interface and web server
  - `planners/`: Planning and decision modules
  - `examples/`: Example agents and workflows
  - `runners/`: Runner classes and orchestration
- Top-level files: `README.md`, `pyproject.toml`, etc.

## 3a. Memory Module Documentation Tasks

- Map out the public API and main classes/functions of the `memory` module:
  - `BaseMemoryService`
  - `InMemoryMemoryService`
  - `VertexAiRagMemoryService`
- Write a module surface overview for `memory/` (similar to agents/tools docs)
- Document usage examples for each memory backend (in-memory, Vertex AI RAG)
- Explain extension points for adding custom memory backends
- Cross-link memory documentation to agents, sessions, and tools where relevant
- Note any code comment or docstring gaps in the memory module
- Add checklist items to the progress log for each of the above

## 3b. Runners Module Documentation Tasks

- Map out the public API and main classes/functions of the `runners` module:
  - `Runner`
  - `InMemoryRunner`
- Write a module surface overview for `runners/` (purpose, responsibilities, integration points)
- Document usage examples:
  - How to instantiate a Runner
  - How to run an agent (sync/async)
  - How to use InMemoryRunner for testing
  - How to use custom artifact/session/memory services
- Explain extension points for customizing runners (subclassing, custom orchestration)
- Cross-link runners documentation to agents, sessions, memory, and artifacts where relevant
- Note any code comment or docstring gaps in the runners module
- Add checklist items to the progress log for each of the above

## 4. Core Concepts

- **Agents:** Types, composition, orchestration
- **Tools:** Built-in tools, custom tools, integration
- **Flows:** Workflow definitions and execution
- **Memory/Sessions:** State management
- **Evaluation:** Testing and benchmarking
- **Deployment:** CLI, web, API, cloud

## 5. CLI Reference

- Main commands:
  - `create`: Scaffold a new agent app
  - `run`: Run an agent interactively
  - `eval`: Evaluate agents
  - `web`: Launch web UI
  - `api_server`: Launch API server
  - `deploy cloud_run`: Deploy to Google Cloud Run
- Example usage for each

## 6. Extending ADK

- Adding new agents, tools, flows, or backends
- Where to find extension points

## 7. API Reference

- What's exposed at the package level
- Key classes and functions

## 8. Examples & Tutorials

- Pointers to `examples/` directory and sample workflows

## CLI Usage Examples (Planned)

- Document usage examples for each main CLI command:
  - `create`
  - `run`
  - `eval`
  - `web`
  - `api_server`
  - `deploy cloud_run`

---

**Next Steps:**

- Map out each major module's public API
- Flesh out each section with details and code samples
- Identify documentation/comment gaps in the codebase
