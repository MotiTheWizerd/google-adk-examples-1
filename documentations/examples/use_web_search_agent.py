import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent
import uuid

from dotenv import load_dotenv
from utils.llm.call_agent_async import call_agent_async
from agents.web_search_agent.web_search_agent import get_web_search_agent
load_dotenv()




async def main():

    # ********** APP SETUP **********
    APP_NAME = "AI Agents Prompt Expert"
    USER_ID = str(uuid.uuid4())
    SESSION_ID = str("session_id_1")
    # ********** END OF APP SETUP **********
       # ********** DATABASE SETUP **********
    db_url = "sqlite:///db_ai_agents_prompt_expert.db"
    session_service = InMemorySessionService()
    # ********** END OF DATABASE SETUP **********

    # ********** SESSION SETUP **********
    intial_state = {
        "user_name": "moti elmakyes",
    }
    session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID, state = intial_state)
    # ********** END OF SESSION SETUP **********
    
    web_serach_agent =get_web_search_agent()

    runner = Runner(app_name=APP_NAME, session_service=session_service, agent=web_serach_agent)

    while True:
        user_input = input("Enter a prompt: ")
        if user_input == "exit":
            break
        else:
            response = await call_agent_async(runner=runner, message=user_input,user_id=USER_ID, session_id=SESSION_ID)
            print(response)
            
   



   
if __name__ == "__main__":
     asyncio.run(main())
  