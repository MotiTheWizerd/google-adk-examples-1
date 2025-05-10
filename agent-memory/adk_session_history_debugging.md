## [2024-08-01] Agent Tool Recognition Issues Caused by Persistent Session History

We faced persistent issues where an `LlmAgent` failed to acknowledge or use a `delete_reminder` tool, despite correct registration and explicit instructions. This persisted even after renaming the tool and simplifying instructions.

**Problem:** An agent using `DatabaseSessionService` did not recognize its _current_ full capabilities when resuming an existing session. It appeared influenced by the conversation history stored within that persistent session, referencing tools or instructions that were present earlier but had since been changed in the code.

**Fix:** Deleting the underlying session database file (`agent_data.db`) forced the creation of a new, clean session. Starting fresh allowed the agent to correctly recognize all currently registered tools based solely on the latest code configuration.

**Lesson:** When debugging ADK agent tool recognition/instruction adherence with persistent sessions, be aware that the agent's context includes the session's conversation history. Resuming old sessions can cause outdated capabilities to linger. Testing with a **fresh session** is crucial for verifying agent behavior against the _current_ code.
