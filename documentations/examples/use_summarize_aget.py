import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.adk.agents import LlmAgent

import uuid

from dotenv import load_dotenv
from utils.llm.call_agent_async import call_agent_async
from agents.summarize_agent.summarize_agent import get_summarize_agent
from utils.sessions.load_user_session import load_user_session
load_dotenv()




async def main():

    # ********** APP SETUP **********c
    APP_NAME = "AI Agents Prompt Expert"
    USER_ID =  "Moti Elmakyes"
    # SESSION_ID = str(uuid.uuid4())
    SESSION_ID = "session_id_1"
    # ********** END OF APP SETUP **********
    intial_state = {
        "urls": [],
    }
    session_details = load_user_session(APP_NAME,USER_ID,SESSION_ID,intial_state)
    session_service = session_details["session_service"]
    SESSION_ID = session_details["session_id"]
    
    summarize_agent =get_summarize_agent()
    

    runner = Runner(app_name=APP_NAME, session_service=session_service, agent=summarize_agent)

    while True:
        user_input = input("Enter a prompt: ")
        if user_input == "exit":
            break
        else:
            response = await call_agent_async(runner=runner, message=user_input,user_id=USER_ID, session_id=SESSION_ID)
            print(response)
            
   



   
if __name__ == "__main__":
     asyncio.run(main())
  