import asyncio
from dotenv import load_dotenv
from google.adk.agents import ParallelAgent,SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import  InMemorySessionService, DatabaseSessionService
import platform
import sys
import socket


from agents.network_system_agent.network_system_agent import get_network_system_agent
from agents.reviewer_agent.reviewer_agent import get_reviewer_agent
from agents.system_info_agent.system_info_agent import get_system_info_agent
from utils.llm.call_agent_async import call_agent_async
from utils.sessions.load_user_session import load_user_session

try:
    import psutil
except ImportError:
    psutil = None


load_dotenv()







async def main():

    # ********** APP SETUP **********
    session_service = InMemorySessionService()
    APP_NAME = "Parallel Agents - System Information"
    USER_ID = "Moti Elmakyes"
    SESSION_ID = "2234567890"
  
    session_details = load_user_session(APP_NAME,USER_ID,SESSION_ID,[])
    SESSION_ID = session_details["session_id"]
    session_service = session_details["session_service"]
    parallel_agent = ParallelAgent(
        name="parallel_agent",
        
        description="A parallel agent that can run multiple agents in parallel",
        sub_agents=[get_system_info_agent(), get_network_system_agent()],
    )

    sequential_agent = SequentialAgent(
        name="sequential_agent",
        description="A sequential agent that can run multiple agents in sequential",
        sub_agents=[parallel_agent, get_reviewer_agent()],
    )


    runner = Runner(app_name=APP_NAME, agent=sequential_agent, session_service=session_service)
    # ********** END OF APP SETUP **********

    while True:
        print("Enter a query:")
        query = input()
        if query == "exit":
            break
        else:
            response = await call_agent_async(runner=runner, message=query,user_id=USER_ID, session_id=SESSION_ID)



if __name__ == "__main__":
    asyncio.run(main())





