import asyncio


#**** GOOGLE ADK IMPORTS ****
from google.adk.agents import LlmAgent
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
#**** END OF GOOGLE ADK IMPORTS ****

#**** UTILS IMPORTS ****
from agents.task_manager_agent.task_planner_agent import get_task_planner_agent
from utils.llm.call_agent_async import call_agent_async
from tools.serper_search_tool import serper_search_tool
#**** END OF UTILS IMPORTS ****

#**** GENERAL IMPORTS ****
import uuid
from dotenv import load_dotenv

#**** END OF GENERAL IMPORTS ****


load_dotenv()



async def main():
    task_planner = get_task_planner_agent()
   
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
    


    
    runner = Runner(app_name=APP_NAME,agent=task_planner,session_service=session_service)

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








