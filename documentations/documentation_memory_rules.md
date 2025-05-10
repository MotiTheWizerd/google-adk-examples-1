# Documentation Memory & Continuity Rules

## Purpose

These rules ensure that documentation work for the ADK project is consistent, easy to resume, and well-organized across sessions and new chats.

---

## 1. Remembering & Resuming Work

** IMPORTENT **
When giving code example always use "gemini-2.0-flash" Model.

- **Always check the `documentions/ADK_documentation_progress.md` file** at the start of any new session or when resuming work. This file tracks what has been completed, what is in progress, and what the next steps are.
- **Review the most recent entries** in the progress log to determine where to pick up.
- **Reference other documentation files** (e.g., `agents_module_surface.md`, `tools_module_surface.md`, `quickstart_draft.md`) for detailed context on what has already been documented.

## 2. Saving Files & Naming Conventions

- **All documentation and progress files must be saved in the `documentations/` folder.**
- **Use clear, descriptive filenames** that reflect the content (e.g., `quickstart_draft.md`, `agents_module_surface.md`).
- **Each major topic or module gets its own file** for clarity and modularity.
- **Each major topic (e.g., CLI usage, Quickstart, module surfaces) should have its own dedicated quickstart or documentation file.**
- **Drafts and in-progress work** should be clearly marked as such in the filename or file header.

## 3. Logging Progress

- **Every significant step or milestone** (e.g., mapping a module, drafting a section) must be logged in `ADK_documentation_progress.md`.
- **Checklists in the progress file** should use `[x]` for completed steps and `[ ]` for pending steps, never deleting old steps.
- **Always update the progress log** before ending a session or when pausing work.

## 4. Starting a New Chat or Session

- **Begin by reading the progress log and recent documentation files** to re-establish context.
- **Summarize the last completed step and the next planned action** before proceeding.
- **If unsure where to resume, consult the checklist and the most recent log entry.**

## 5. General Documentation Practices

- **Write documentation as if for a teammate:** clear, practical, and with enough context for someone new to pick up the work.
- **Comment or annotate drafts** with TODOs or open questions if something is incomplete or needs review.
- **Keep documentation modular**—each file should cover a single topic or module as much as possible.

---

_These rules should be followed automatically whenever documentation work is resumed, a new chat starts, or memory is referenced._
