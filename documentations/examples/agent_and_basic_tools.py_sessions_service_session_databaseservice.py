"""
main.py

Entry point for the ADK agent framework demo.

This script initializes the application session, sets up the root LlmAgent, and configures the in-memory session service for state management. It also demonstrates how to register a sub-agent (web_searcher_agent) for modular agent composition.

Key responsibilities:
- Loads environment variables for configuration.
- Defines initial user state and preferences.
- Creates a unique session and user ID for each run.
- Instantiates the root agent and attaches it to the session.
- Sets up the ADK Runner to manage agent execution and session lifecycle.

Intended for quick prototyping, testing, or as a reference for integrating ADK agents in a modular, extensible way.
"""

# Import the core LlmAgent class from ADK
from google.adk.agents import LlmAgent
# Import a custom sub-agent (not used in this script, but shows modularity)
from agents.web_searcher_agent.web_searcher_agent import web_searcher_agent
# Import session and runner utilities from ADK
from google.adk.runners import  Runner
from google.adk.sessions import DatabaseSessionService
# Import types for message content
from google.genai import types
# For loading environment variables from a .env file
from dotenv import load_dotenv
# Custom callback for pre-model logic (not used here, but available)
from utils.before_model_callback import before_model_callback
# Utility for async agent calls (not used here, but available)
# from utils.llm.call_sequential_agent_async import call_sequential_agent_async
# For generating unique IDs
from utils.llm.call_agent_async import call_agent_async
from google.adk.tools import ToolContext
import uuid
# For JSON serialization (not used directly here)
import json
# For async operations (not used directly here)
import asyncio


# Load environment variables from .env (API keys, config, etc.)
load_dotenv()

def add_reminder(parameters: dict, tool_context: ToolContext) -> dict:
    """
    Adds a reminder to the user's list of reminders in the session state.

    Args:
        parameters (dict): Dictionary containing the reminder text in the 'reminder' field.
        tool_context (ToolContext): The context object containing the current session state.

    Returns:
        dict: A dictionary with action details and a confirmation message.
    """
    # Check if parameters is nested inside another dict (which happens in function calls)
    if "parameters" in parameters:
        parameters = parameters["parameters"]
        
    reminder = parameters.get("reminder")
    print(f"Adding reminder: {reminder}")
    
    reminders = tool_context.state.get("reminders", [])
    reminders.append(reminder)
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Reminder '{reminder}' added successfully."
    }


def show_reminders(parameters: dict, tool_context: ToolContext) -> dict:
    """
    Retrieves the list of reminders from the session state.

    Args:
        parameters (dict): Not used in this function, but part of the standard tool signature.
        tool_context (ToolContext): The context object containing the current session state.

    Returns:
        dict: A dictionary containing the list of reminders.
    """
    reminders = tool_context.state.get("reminders", [])
    print(f"Showing reminders: {reminders}")

    # Format reminders with numbers for display
    if reminders:
        numbered_reminders = [f"{i+1}. {r}" for i, r in enumerate(reminders)]
        message = f"Here are your current reminders:\n" + "\n".join(numbered_reminders)
    else:
        message = "You have no reminders."

    return {
        "action": "show_reminders",
        "reminders": reminders,
        "message": message
    }


def update_reminder(parameters: dict, tool_context: ToolContext) -> dict:
    """
    Updates a reminder at a specific index in the user's list.

    Args:
        parameters (dict): Dictionary containing 'index' (1-based) and 'new_reminder' text.
        tool_context (ToolContext): The context object containing the current session state.

    Returns:
        dict: A dictionary confirming the update or reporting an error.
    """
    # Handle potential nesting
    if "parameters" in parameters:
        parameters = parameters["parameters"]
        
    try:
        index = int(parameters.get("index"))
        new_reminder = parameters.get("new_reminder")
    except (ValueError, TypeError):
        return {"error": "Invalid index provided. Please provide a number."}

    if not new_reminder:
        return {"error": "No new reminder text provided."}

    reminders = tool_context.state.get("reminders", [])

    # Convert 1-based index to 0-based index
    actual_index = index - 1

    if 0 <= actual_index < len(reminders):
        old_reminder = reminders[actual_index]
        reminders[actual_index] = new_reminder
        tool_context.state["reminders"] = reminders
        print(f"Updating reminder {index}: '{old_reminder}' to '{new_reminder}'")
        return {
            "action": "update_reminder",
            "index": index,
            "old_reminder": old_reminder,
            "new_reminder": new_reminder,
            "message": f"Reminder {index} updated successfully from '{old_reminder}' to '{new_reminder}'."
        }
    else:
        print(f"Invalid index {index} provided for update.")
        return {
            "error": f"Invalid index: {index}. Please use 'show_reminders' to see valid indices."
        }


def delete_reminder(parameters: dict, tool_context: ToolContext) -> dict:
    """
    Deletes a reminder at a specific index from the user's list.

    Args:
        parameters (dict): Dictionary containing the 'index' (1-based) of the reminder to delete.
        tool_context (ToolContext): The context object containing the current session state.

    Returns:
        dict: A dictionary confirming the deletion or reporting an error.
    """
    # Handle potential nesting
    if "parameters" in parameters:
        parameters = parameters["parameters"]

    try:
        index = int(parameters.get("index"))
    except (ValueError, TypeError):
        return {"error": "Invalid index provided. Please provide a number."}

    reminders = tool_context.state.get("reminders", [])

    # Convert 1-based index to 0-based index
    actual_index = index - 1

    if 0 <= actual_index < len(reminders):
        deleted_reminder = reminders.pop(actual_index)
        tool_context.state["reminders"] = reminders
        print(f"Deleting reminder {index}: '{deleted_reminder}'")
        return {
            "action": "delete_reminder",
            "index": index,
            "deleted_reminder": deleted_reminder,
            "message": f"Reminder {index} ('{deleted_reminder}') deleted successfully."
        }
    else:
        print(f"Invalid index {index} provided for deletion.")
        return {
            "error": f"Invalid index: {index}. Please use 'show_reminders' to see valid indices."
        }


def change_user_name(parameters: dict, tool_context: ToolContext) -> dict:
    """
    Changes the user's name in the session state.

    Args:
        parameters (dict): Dictionary containing the 'new_name'.
        tool_context (ToolContext): The context object containing the current session state.

    Returns:
        dict: A dictionary confirming the name change.
    """
    # Handle potential nesting
    if "parameters" in parameters:
        parameters = parameters["parameters"]

    new_name = parameters.get("new_name")

    if not new_name:
        return {"error": "No new name provided."}

    old_name = tool_context.state.get("user_name", "Unknown")
    tool_context.state["user_name"] = new_name
    print(f"Changing user name from '{old_name}' to '{new_name}'")

    return {
        "action": "change_user_name",
        "old_name": old_name,
        "new_name": new_name,
        "message": f"User name changed successfully from '{old_name}' to '{new_name}'."
    }


async def main():
    # Define the initial state for the session, including user info and preferences
    initial_state = {
        "user_name": "Moti Elmakayes",
        "reminders" : []
    }

    db_url = "sqlite:///agent_data.db"
    # Create a session service to manage in-memory  session state
    session_service = DatabaseSessionService(db_url=db_url)
    # Set up app/session/user identifiers
    APP_NAME = "Database Memory Service app"
    SESSION_ID = str(uuid.uuid4())  # Unique session ID for this run
    USER_ID ="Moti_Elmakayes"    # Unique user ID for this run
     
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    if existing_sessions and len(existing_sessions.sessions) > 0:
        print(f"Resuming session {existing_sessions.sessions[0].id}")
        SESSION_ID = existing_sessions.sessions[0].id
    else:
        print(f"Creating new session {SESSION_ID}")
        session = session_service.create_session(
        app_name=APP_NAME,
        session_id=SESSION_ID,
        user_id=USER_ID,
        state=initial_state,
    )

    # Instantiate the root agent with a name, model, and instructions
    root_agent = LlmAgent(
        name="root_agent",
        model="gemini-2.0-flash",
        instruction="""
    you are a helpful assistant that can help with reminders and manage your user name.
    - User's Current Name: {user_name}
    - Current Reminders: {reminders}

    **Reminder Management:**
    *   To **add** a reminder, use the `add_reminder` tool with the `reminder` text.
    *   To **show** all reminders (with numbers), use the `show_reminders` tool.
    *   To **update** a reminder, use the `update_reminder` tool. Provide the `index` (number from `show_reminders`) and the `new_reminder` text.
    *   To **delete** a reminder, use the `delete_reminder` tool. Provide the `index` (number from `show_reminders`) of the reminder to remove.

    **User Name Management:**
    *   To **change** the user name, use the `change_user_name` tool with the `new_name`.

    **Important:** Always confirm actions back to the user. When showing reminders, list them clearly with numbers.

    ALWAYS use the `delete_reminder` tool when asked to delete or remove a reminder by its number.

    *** TOOLS LIST ***
    - add_reminder
    - show_reminders
    - update_reminder
    - delete_reminder
    - change_user_name
    """,
    tools=[add_reminder, show_reminders, update_reminder, delete_reminder, change_user_name]
    )

    print("Registered tools:", [tool.name for tool in root_agent.canonical_tools])
    # Create the ADK runner to manage agent execution and session lifecycle
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    print('initializing runner')
    
    # Interactive conversation loop
    while True:
        # Get user input
        message = input("Enter a message: ")
        if message.lower() == "exit":
            break
            
        print(f"Sending message to agent: {message}")
        # Call the agent and get the response
        response = await call_agent_async(runner, user_id=USER_ID, session_id=SESSION_ID, message=message)
        
        # Print the final response
        # print(f"Agent response: {response}")
        
        # Optionally, print current reminders from state
        session = session_service.get_session(
            app_name=APP_NAME,
            session_id=SESSION_ID,
            user_id=USER_ID
        )
        if session and session.state:
            reminders = session.state.get("reminders", [])
            print(f"Current reminders: {reminders}")
            
    print("Conversation ended.")


if __name__ == "__main__":
    # Run the main function if this script is executed directly
    asyncio.run(main())