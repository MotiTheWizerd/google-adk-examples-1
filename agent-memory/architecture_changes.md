## [2024-06-09] Directory Structure and **init**.py for ADK Agents

We encountered an `AttributeError: module 'agents' has no attribute 'agent'` when running an agent with ADK web. The root cause was missing `__init__.py` files in the `agents/` and/or agent subdirectories, which prevented Python from recognizing them as packages.

**Solution:** Ensure both `agents/` and each agent subfolder (e.g., `greeting_agent/`) have an `__init__.py` file. This enables proper package recognition and allows ADK to import agent modules as expected.

**Lesson:** Always verify directory structure and package initialization files when building modular agent systems with ADK.
