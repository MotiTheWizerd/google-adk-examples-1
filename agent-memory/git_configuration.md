## [2024-07-30] Created .gitignore to Exclude adk/ Folder

Created a `.gitignore` file at the project root to prevent the `adk/` directory and other common artifacts from being tracked by Git.

**Problem:** The `adk/` folder, likely containing external library code, should not be committed to the project's version control. Additionally, other generated files (like Python bytecode, virtual environments, IDE settings) can clutter the repository.

**Fix:**

1.  A new file named `.gitignore` was created in the workspace root.
2.  The primary entry added was `adk/` to ignore the Google Agent Developer Kit directory.
3.  The following common patterns were also included for a typical Python project:
    - **Python artifacts:** `__pycache__/`, `*.py[cod]`, `*$py.class`
    - **Virtual environments:** `.env`, `.venv`, `env/`, `venv/`, `ENV/`, `*/activate_this.py`
    - **IDE specific files:** `.vscode/`, `.idea/`, `*.sublime-project`, `*.sublime-workspace`
    - **OS specific files:** `.DS_Store`, `Thumbs.db`

**Lesson:** A well-configured `.gitignore` file is essential for good version control hygiene. It prevents unnecessary files from being tracked, reduces repository size, and avoids conflicts related to user-specific or generated files. Always include ignores for vendor directories, build artifacts, environment folders, and common OS/IDE files relevant to the project stack.
