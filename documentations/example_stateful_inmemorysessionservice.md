# Example: Using Stateful InMemorySessionService with ADK

This example demonstrates how to use the ADK's `InMemorySessionService` to manage stateful agent sessions. It covers the full workflow: creating the session service, initializing a session, setting up an agent and runner, sending a user message, and printing the agent's response.

---

## What This Example Shows

- How to create and configure an `InMemorySessionService` for stateful session management.
- How to initialize a session with user-specific state (e.g., name, preferences).
- How to instantiate an agent and attach it to a session.
- How to use the ADK `Runner` to process user messages and stream agent responses.
- How to retrieve and inspect session state after agent interaction.

---

## Example Code

```python
from google.adk.agents import LlmAgent
from google.adk.runners import InMemorySessionService, Runner
from google.genai import types
import uuid

# 1. Define initial user state
initial_state = {
    "user_name": "Moti Elmakayes",
    "user_preferences": """
        I am Moti Elmakayes, I am a software engineer, I like to learn new things and I like to share my knowledge with others.
        I am interested in AI, Machine Learning, and Web Development.
        I am also interested in the stock market and the news related to it.
        and love to play basketball in my free time.
        I am a big fan of the New York Knicks.
    """
}

# 2. Create the session service
session_service = InMemorySessionService()

# 3. Generate unique IDs for app, session, and user
APP_NAME = "Demo app"
SESSION_ID = str(uuid.uuid4())
USER_ID = str(uuid.uuid4())

# 4. Create a new session with the initial state
session = session_service.create_session(
    app_name=APP_NAME,
    session_id=SESSION_ID,
    user_id=USER_ID,
    state=initial_state,
)

# 5. Instantiate the agent
root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are a helpful assistant that can answer questions.
        Here is some information about our user:
        user name: {user_name}
        user preferences: {user_preferences}
    """
)

# 6. Set up the runner
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service,
)

# 7. Send a user message and print the agent's answer
message = "tell me about moti's interests"
new_message = types.Content(role="user", parts=[types.Part(text=message)])
for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=new_message):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(event.content.parts[0].text)

# 8. Retrieve and print session state after interaction
session_details = session_service.get_session(
    app_name=APP_NAME,
    session_id=SESSION_ID,
    user_id=USER_ID
)
print("Session details:")
for key, value in session_details.state.items():
    print(f"{key}: {value}")
```

---

## Key Points

- The `InMemorySessionService` allows you to manage per-user, per-session state in memory—ideal for prototyping and testing.
- Each session is uniquely identified by app, session, and user IDs.
- The agent can access user state via formatted instructions.
- The runner streams events, so you can handle partial or final responses as needed.
- After running, you can inspect the session state for debugging or further logic.

---

## When to Use This Pattern

- Prototyping new agents or workflows
- Testing agent logic with different user states
- Demos or quick experiments where persistent storage is not required

---

## See Also

- `documentations/runners_module_surface.md` for more on the Runner
- `documentations/memory_module_surface.md` for memory/state management details
- ADK source: `adk/runners/inmemory_session_service.py` for implementation details
