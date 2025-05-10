# ADK Agents Module: Public API & Surface Overview

## Purpose

This document summarizes the public API and main classes of the `agents` module in the Agent Development Kit (ADK). It is intended as a reference for documentation and onboarding.

---

## What is Exposed (from `agents/__init__.py`)

- `Agent` (alias for `LlmAgent`)
- `BaseAgent`
- `LlmAgent`
- `LoopAgent`
- `ParallelAgent`
- `SequentialAgent`

## Main Classes & Their Roles

### 1. `BaseAgent`

- **Description:** The abstract base class for all agents in ADK.
- **Key Features:**
  - Defines agent hierarchy (parent/sub-agents)
  - Provides async run methods (`run_async`, `run_live`)
  - Supports before/after callbacks
  - Methods for finding agents in the tree
- **Usage:** Inherit to create custom agent types.

### 2. `LlmAgent` (aliased as `Agent`)

- **Description:** The main agent type for LLM-based workflows.
- **Key Features:**
  - Inherits from `BaseAgent`
  - Configurable with model, instructions, tools, planner, code executor, etc.
  - Supports global and per-agent instructions
  - Can restrict agent transfer, control input/output schemas
  - Supports before/after model callbacks
- **Usage:** Most user agents will be `LlmAgent` or its alias `Agent`.

### 3. `LoopAgent`

- **Description:** Runs its sub-agents in a loop until a condition is met (e.g., escalation or max iterations).
- **Key Features:**
  - Inherits from `BaseAgent`
  - Useful for repeated or iterative workflows

### 4. `ParallelAgent`

- **Description:** Runs its sub-agents in parallel, each in isolation.
- **Key Features:**
  - Inherits from `BaseAgent`
  - Useful for scenarios needing multiple perspectives or attempts

### 5. `SequentialAgent`

- **Description:** Runs its sub-agents in sequence.
- **Key Features:**
  - Inherits from `BaseAgent`
  - Useful for pipeline-style workflows

## Supporting Classes (not all are public, but important for context)

- `LiveRequest`, `LiveRequestQueue`: For live/streaming agent interactions
- `RunConfig`: Runtime configuration for agents
- `CallbackContext`, `ReadonlyContext`, `InvocationContext`: Context objects for agent execution and callbacks
- `TranscriptionEntry`: For audio/data transcription in agent runs

## Relationships

- All agent types inherit from `BaseAgent`.
- Agents can have sub-agents (tree structure), enabling composition.
- `LlmAgent` is the primary agent for LLM-based tasks, but shell agents (`LoopAgent`, `ParallelAgent`, `SequentialAgent`) orchestrate other agents.

---

## Next Steps

- Document example usage for each agent type
- Map out extension points and custom agent creation
- Cross-link to tools and flows documentation
