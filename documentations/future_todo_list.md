# ADK Future TODO List

This file tracks known TODOs, documentation gaps, and areas for future improvement in the codebase.

---

## Outstanding TODOs and Documentation Gaps

### 1. `src/google/adk/tools/function_tool.py`

- `# TODO(hangfei): fix call live for function stream.`
  - The `_call_live` method is not fully implemented for function streaming.

### 2. `src/google/adk/tools/function_parameter_parse_util.py`

- `# TODO(kech): Remove this workaround once mldev supports default value.`
  - There is a workaround for default value handling that should be removed once upstream support is available.

### 3. `src/google/adk/tools/application_integration_tool/application_integration_toolset.py`

- `# TODO(cheliu): Apply a common toolset interface`
  - The toolset should implement a common interface for consistency.

### 4. Utility and Helper Functions

- Some utility/helper functions (especially private ones) lack detailed docstrings or inline comments explaining tricky logic.
- Expand docstrings for public classes/methods that are currently minimal or missing.

### 5. Error Handling and Workarounds

- Add comments explaining error handling, edge cases, and workarounds (e.g., why certain exceptions are raised, or why a workaround is in place).

---

Add new TODOs and documentation gaps here as they are discovered.
