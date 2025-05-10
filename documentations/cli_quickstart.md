# ADK CLI Quickstart

This guide covers usage examples for the main ADK CLI commands. Each example includes basic usage, options, and practical tips.

---

## 1. Create a New Agent App

Scaffold a new agent app in a target directory. This sets up a minimal agent template with the necessary files.

```bash
adk create path/to/my_app
```

**Options:**

- `--model`: (Optional) Specify the model for the root agent (e.g., `gemini-2.0-pro`)
- `--api_key`: (Optional) Google AI API Key for Gemini models
- `--project`: (Optional) Google Cloud Project (for VertexAI backend)
- `--region`: (Optional) Google Cloud Region (for VertexAI backend)

**Example with options:**

```bash
adk create my_agent --model=gemini-2.0-pro --api_key=YOUR_API_KEY
```

> Tip: The command will prompt for missing required info (like model or API key) if not provided.

## 2. Run an Agent Interactively

Run an agent in interactive CLI mode. This lets you chat with your agent directly from the terminal.

```bash
adk run path/to/your_agent
```

**Options:**

- `--save_session`: (Optional) Save the session to a JSON file on exit.
- `--replay <file>`: (Optional) Start a session from a JSON file containing initial state and queries (no further interaction).
- `--resume <file>`: (Optional) Resume a previously saved session from a JSON file.

**Example with session saving:**

```bash
adk run my_agent --save_session
```

> Tip: Use `--save_session` to capture your conversation for later review or to continue it later with `--resume`.

## 3. Evaluate an Agent

Run evaluation sets against your agent to benchmark or test its performance.

```bash
adk eval path/to/agent/__init__.py path/to/eval_set.json
```

**Options:**

- `--config_file_path <file>`: (Optional) Path to a config file with evaluation criteria.
- `--print_detailed_results`: (Optional) Print detailed results to the console.

**Example with multiple eval sets and detailed results:**

```bash
adk eval my_agent/__init__.py evals/set1.json evals/set2.json --print_detailed_results
```

> Tip: To run only specific evals from a set, use the syntax `eval_set.json:eval_1,eval_2` as an argument.

## 4. Launch the Web UI

Start a FastAPI server with a web UI for your agents. Great for local development and testing.

```bash
adk web path/to/agents_dir
```

**Options:**

- `--session_db_url <url>`: (Optional) Database URL for storing sessions (e.g., SQLite or Agent Engine).
- `--port <port>`: (Optional) Port for the server (default: 8000).
- `--allow_origins <origin>`: (Optional, repeatable) Additional origins to allow for CORS.
- `--log_level <level>`: (Optional) Set logging level (DEBUG, INFO, etc.).
- `--log_to_tmp`: (Optional) Log to system temp folder instead of console.
- `--trace_to_cloud`: (Optional) Enable cloud trace for telemetry.

**Example with custom port and DB:**

```bash
adk web my_agents --session_db_url=sqlite:///my_sessions.db --port=8080
```

> Tip: Use `--allow_origins` if you're developing a frontend on a different port or domain and need to avoid CORS issues.

## 5. Start the API Server

Start a FastAPI server for your agents (API only, no web UI). Use this for production or when integrating with other services.

```bash
adk api_server path/to/agents_dir
```

**Options:**

- `--session_db_url <url>`: (Optional) Database URL for storing sessions.
- `--port <port>`: (Optional) Port for the server (default: 8000).
- `--allow_origins <origin>`: (Optional, repeatable) Additional origins to allow for CORS.
- `--log_level <level>`: (Optional) Set logging level.
- `--log_to_tmp`: (Optional) Log to system temp folder instead of console.
- `--trace_to_cloud`: (Optional) Enable cloud trace for telemetry.

**Example with custom port and DB:**

```bash
adk api_server my_agents --session_db_url=sqlite:///my_sessions.db --port=9000
```

> Tip: Use `api_server` when you want a backend API without the web UI. The endpoints are compatible with the web UI, so you can switch between them as needed.

## 6. Deploy to Google Cloud Run

Deploy your agent as a managed service on Google Cloud Run. This packages your agent and launches it in the cloud.

```bash
adk deploy cloud_run --project=<project> --region=<region> path/to/my_agent
```

**Options:**

- `--project <project>`: (Required) Google Cloud project to deploy to.
- `--region <region>`: (Required) Google Cloud region for deployment.
- `--service_name <name>`: (Optional) Name for the Cloud Run service.
- `--app_name <name>`: (Optional) App name for the ADK API server.
- `--port <port>`: (Optional) Port for the API server (default: 8000).
- `--trace_to_cloud`: (Optional) Enable Cloud Trace for monitoring.
- `--with_ui`: (Optional) Deploy with the web UI (default is API server only).
- `--temp_folder <path>`: (Optional) Temp folder for build files.
- `--verbosity <level>`: (Optional) Set CLI verbosity (debug, info, etc.).
- `--session_db_url <url>`: (Optional) Database URL for session storage.

**Example with required options:**

```bash
adk deploy cloud_run --project=my-gcp-project --region=us-central1 my_agent
```

> Tip: Add `--with_ui` to deploy the web UI along with the API server. By default, only the API server is deployed.

---

<!-- TODO: Add usage examples for: run, eval, web, api_server, deploy cloud_run -->
