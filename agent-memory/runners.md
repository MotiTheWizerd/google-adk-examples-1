## [2024-06-09] Always Use run_async with ADK Runners

When invoking agent runners, always use the run_async method instead of run. This ensures asynchronous event streaming and proper session handling, which is required for correct ADK agent operation.

**Problem:** Using run instead of run_async can break event streaming and may not align with ADK's async workflow.
**Fix:** Standardize on run_async for all runner calls.
**Lesson:** Always check for async/streaming methods in ADK runners and prefer them for agent communication.
