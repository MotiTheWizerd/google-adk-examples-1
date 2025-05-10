import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService,DatabaseSessionService
from google.adk.agents import LlmAgent,SequentialAgent
import uuid

from dotenv import load_dotenv
from agents.query_generation_agent.query_generation_agent import get_query_generation_agent
from agents.reviewer_agent.reviewer_agent import get_reviewer_agent
from agents.single_page_scraper_agent.single_page_scraper_agent import get_web_scrape_single_page_agent
from agents.summarize_agent.summarize_agent import get_summarize_agent
from utils.llm.call_agent_async import call_agent_async
from agents.web_search_agent.web_search_agent import get_web_search_agent
from utils.sessions.load_user_session import load_user_session
load_dotenv()




async def main():

    # ********** APP SETUP **********
    APP_NAME = "AI Agents Prompt Expert"
    USER_ID =  "Moti Elmakyes"
    SESSION_ID =str(uuid.uuid4())
    # ********** END OF APP SETUP **********
       # ********** DATABASE SETUP **********
    intial_state = {
        "urls": [],
    }
    session_details = load_user_session(APP_NAME,USER_ID,SESSION_ID,intial_state)
    session_service = session_details["session_service"]
    SESSION_ID = session_details["session_id"]
    # ********** END OF SESSION SETUP **********
    web_serach_agent =get_web_search_agent()
    web_scrape_single_page_agent = get_web_scrape_single_page_agent()
    query_generation_agent = get_query_generation_agent()
    summarize_agent = get_summarize_agent()
    reviewer_agent = get_reviewer_agent()
    sequential_agent = SequentialAgent(
        name="sequential_agent",
        description="a sequential agent that is charge on execute other agents in a specific order",
        sub_agents=[query_generation_agent,
                    web_serach_agent,  
                    web_scrape_single_page_agent, 
                    reviewer_agent],
      
       
    )
    runner = Runner(app_name=APP_NAME, session_service=session_service, agent=sequential_agent)

    while True:
        user_input = input("Enter a prompt: ")
        if user_input == "exit":
            break
        else:
            response = await call_agent_async(runner=runner, message=user_input,user_id=USER_ID, session_id=SESSION_ID)
            print(response)
            
   



   
if __name__ == "__main__":
     asyncio.run(main())
  