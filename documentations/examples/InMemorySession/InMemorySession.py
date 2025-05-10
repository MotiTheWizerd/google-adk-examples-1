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
from google.adk.runners import InMemorySessionService, Runner
# Import types for message content
from google.genai import types
# For loading environment variables from a .env file
from dotenv import load_dotenv
# Custom callback for pre-model logic (not used here, but available)
from utils.before_model_callback import before_model_callback
# Utility for async agent calls (not used here, but available)
from utils.llm.call_sequential_agent_async import call_sequential_agent_async
# For generating unique IDs
import uuid
# For JSON serialization (not used directly here)
import json
# For async operations (not used directly here)
import asyncio

# Load environment variables from .env (API keys, config, etc.)
load_dotenv()


def main():
    # Define the initial state for the session, including user info and preferences
    initial_state = {
        "user_name": "Moti Elmakayes",
        "user_preferences": """
    I am Moti Elmakayes, I am a software engineer, I like to learn new things and I like to share my knowledge with others.
    I am interested in AI, Machine Learning, and Web Development.
    I am also interested in the stock market and the news related to it.
    I am interested in the news related to the stock market.
    and love to play basketball in my free time.
    I am a big fan of the New York Knicks.
"""
    }

    # Create a session service to manage in-memory session state
    session_service = InMemorySessionService()
    # Set up app/session/user identifiers
    APP_NAME = "Demo app"
    SESSION_ID = str(uuid.uuid4())  # Unique session ID for this run
    USER_ID = str(uuid.uuid4())     # Unique user ID for this run

    # Create a new session with the initial state
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
    You are a helpful assistant that can answer questions.
    hhere is some information about our user:
    user name: {user_name}
    ----------------------------------
    user preferences: {user_preferences}
    """
    )

    # Create the ADK runner to manage agent execution and session lifecycle
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    # Example user message to send to the agent
    message = "tell me about moti's interests"
    # Wrap the message in the required types.Content structure
    new_message = types.Content(role="user", parts=[types.Part(text=message)])
    # Run the agent with the message, streaming events as they arrive
    for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=new_message):
        # Check if this is the final response from the agent
        if event.is_final_response():
            # If the response has content, print the first part's text
            if event.content and event.content.parts:
                print(event.content.parts[0].text)

    session_details = session_service.get_session(
        app_name=APP_NAME,
        session_id=SESSION_ID,
        user_id=USER_ID
    )
    print("Session details:")
    for key, value in session_details.state.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    # Run the main function if this script is executed directly
    main()