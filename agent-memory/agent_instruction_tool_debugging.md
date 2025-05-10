## [2024-08-01] Iterative Debugging for Agent Tool Non-Compliance

Encountered an agent consistently failing to use a correctly implemented/registered tool (`delete_reminder`), despite multiple instruction refinements.

**Problem:** Agent denied capability despite tool registration and instructions mentioning it.

**Debugging Steps Tried:**

1.  Explicit Instructions (increasing specificity).
2.  Keyword Change (delete -> remove -> unshow).
3.  Instruction Simplification & Tool Isolation.

**Root Cause Discovery:** Initial steps failed. Issue identified as interference from **persistent session history** (`DatabaseSessionService`) causing recall of outdated tool configurations.

**Lesson:** When an agent fails instruction/tool usage:

- Consider context beyond current code (like session history).
- If using persistent sessions, test with a **fresh session** to eliminate historical influence.
- Instruction phrasing isn't always the root cause; check the full context.
