import asyncio


#**** GOOGLE ADK IMPORTS ****
from google.adk.agents import LlmAgent
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
#**** END OF GOOGLE ADK IMPORTS ****

#**** UTILS IMPORTS ****
from agents.team_manager_agent.team_manager_agent import get_team_manager
from utils.llm.call_agent_async import call_agent_async
from tools.serper_search_tool import serper_search_tool
#**** END OF UTILS IMPORTS ****

#**** GENERAL IMPORTS ****
import uuid
from dotenv import load_dotenv
#**** END OF GENERAL IMPORTS ****
load_dotenv()
from datetime import datetime



def get_current_time() -> str:
    """
    Get the current system time formatted as 'dd/MM/yyyy HH:mm:ss'.

    Returns:
        str: The current time in the format 'day/month/year hour:minute:second'.
    
    Example:
        >>> get_current_time()
        '28/07/2024 15:42:10'
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


async def main():
    time_agent = LlmAgent(
    name="get_current_time_agent",
    description="Agent that can tell the current time.",
    instruction="Use the current_time tool to provide the current time.",
    model="gemini-2.0-flash",  # or your preferred model
    tools=[get_current_time],
    output_key="current_time"
    )
    
    search_agent = LlmAgent(
        name="web_search_agent",
        description="Agent that can perform web searches using the serper_search_tool.",
        instruction="Use the serper_search_tool to find information on the web based on the user's query.",
        model="gemini-2.0-flash",  # or your preferred model
        tools=[serper_search_tool],
        output_key="search_results"
    )
    
    team_manager = get_team_manager([time_agent, search_agent])
 
    db_url = "sqlite:///agent_data.db"
    session_service = DatabaseSessionService(db_url)

    USER_ID = "moti elmakyes"
    SESSION_ID = str(uuid.uuid4())
    APP_NAME = "testing app"

    state = {
        "results": []
    }
    session = session_service.create_session(app_name=APP_NAME,
                                             user_id=USER_ID,
                                               session_id=SESSION_ID,
                                               state=state)
    


    
    runner = Runner(app_name=APP_NAME,agent=team_manager,session_service=session_service)

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = await call_agent_async(runner,user_id=USER_ID,
                                     session_id=SESSION_ID,
                                     message=user_input)
                                     
        print(response)

if __name__ == "__main__":
    asyncio.run(main())








