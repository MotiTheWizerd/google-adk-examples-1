import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.adk.agents import LlmAgent

import uuid

from dotenv import load_dotenv
from utils.llm.call_agent_async import call_agent_async
from agents.single_page_scraper_agent.single_page_scraper_agent import get_web_scrape_single_page_agent
load_dotenv()




async def main():
    db_url = "sqlite:///db_ai_agents_prompt_expert.db"
    # ********** APP SETUP **********
    APP_NAME = "AI Agents Prompt Expert"
    USER_ID =  "Moti Elmakyes"
    # SESSION_ID = str(uuid.uuid4())
    SESSION_ID = "session_id_1"
    # ********** END OF APP SETUP **********
       # ********** DATABASE SETUP **********
    
    session_service = DatabaseSessionService(db_url)
    # ********** END OF DATABASE SETUP **********

    # ********** SESSION SETUP **********
    
    # is_session_exists = session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
    # print(is_session_exists)
    session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    intial_state = {
        "urls": ["https://www.newyorktimes.com","https://www.reddit.com"],
    }
    if session is None:
       session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID, state=intial_state)
       
    else:
       SESSION_ID = session.id
       print("Loaded existing session, state updated:", session.id)
    # ********** END OF SESSION SETUP **********
    
    scrape_agent =get_web_scrape_single_page_agent()
    scrape_agent.output_key = "web_scrape_single_page_results"
    runner = Runner(app_name=APP_NAME, session_service=session_service, agent=scrape_agent)

    while True:
        user_input = input("Enter a prompt: ")
        if user_input == "exit":
            break
        else:
            response = await call_agent_async(runner=runner, message=user_input,user_id=USER_ID, session_id=SESSION_ID)
            print(response)
            
   



   
if __name__ == "__main__":
     asyncio.run(main())
  