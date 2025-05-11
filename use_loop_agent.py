import asyncio
import uuid
from dotenv import load_dotenv
from google.adk.agents import SequentialAgent, LoopAgent
from google.adk.runners import Runner
from agents.python_expert_agent.python_expert_agent import get_python_expert_agent
from agents.python_refiner_agent.python_refiner_agent import get_python_refiner_agent
from utils.llm.call_agent_async import call_agent_async
from utils.sessions.load_user_session import load_user_session
from agents.python_reviewer_agent.python_reviewer_agent import get_python_reviewer_agent

load_dotenv()


async def main():
    

    APP_NAME = "Working with Loop Agent"
    SESSION_ID = str(uuid.uuid4())
    USER_ID = "user123"
    initial_state = {
        "generated_code" : ""
    }
    sessionDetails = load_user_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID, intial_state=initial_state)
    SESSION_ID = sessionDetails["session_id"]
    session_service = sessionDetails["session_service"]


    # Create a loop agent
    loop_agent = LoopAgent(
        name="loop_agent",
        description="A loop agent that can loop through a list of items",
        max_iterations=5,
        sub_agents=[get_python_reviewer_agent(), get_python_refiner_agent()]
    )

    python_expert_agent = get_python_expert_agent()
    # Create a sequential agent
    sequential_agent = SequentialAgent(
        name="sequential_agent",
        description="A sequential agent that can execute a list of agents in order",
        sub_agents=[get_python_expert_agent(), loop_agent]
    )
    runner = Runner(app_name=APP_NAME, agent=sequential_agent, session_service=session_service)
    while True:
        user_input = input("Enter a message: ")
        if user_input == "exit":
            break
        else:
            response = await call_agent_async(runner=runner,
                                 user_id=USER_ID, 
                                 session_id=SESSION_ID, 
                                 message=user_input)
            print(response)



if __name__ == "__main__":
     asyncio.run(main())
  

 







