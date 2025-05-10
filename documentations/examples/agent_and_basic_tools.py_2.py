import asyncio
import uuid
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from utils.llm.call_agent_async import call_agent_async


load_dotenv()




def add_numbers(a: int, b: int, tool_context: ToolContext) -> int:
    tool_context.state["reminders"] = "hello world"
    return a + b


async def main():
    db_url = "sqlite:///agent_data.db"
    session_service = DatabaseSessionService(db_url)

    USER_ID = "moti elmakyes"
    SESSION_ID = str(uuid.uuid4())
    APP_NAME = "testing app"


    agent = LlmAgent(
        name = "personal_assistant",
        model="gemini-2.0-flash",
        instruction="""You are a helpful assistant that can answer questions and help with tasks.
        you have tools stack at your disposal:
        -- TOOLS LIST --
        add_numbers: add two numbers together.
        """,
        tools=[add_numbers]

    )



    session = session_service.create_session(app_name=APP_NAME,user_id=USER_ID, session_id=SESSION_ID)
    
   

    runner = Runner(app_name=APP_NAME,agent=agent,session_service=session_service)



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
    main()


