import asyncio
from typing import Optional, Union
import uuid
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.adk.agents import LlmAgent
from dotenv import load_dotenv
from adk.tools.tool_context import ToolContext
from utils.llm.call_agent_async import call_agent_async
import logging
from agents.query_generation_agent.query_generation_agent import get_query_generation_agent

# Suppress the specific ADK warning about non-text parts when event.text is accessed
logging.getLogger("google.adk.runtime.event").setLevel(logging.ERROR)

load_dotenv()

dbURL = "sqlite:///agent_test_1.db"
session_service = DatabaseSessionService(dbURL)
APP_NAME = "Learning"
USER_ID = "123"
SESSION_ID =  str(uuid.uuid4())



session = session_service.create_session(
    app_name=APP_NAME,
    session_id=SESSION_ID,
    user_id=USER_ID,
     state = []
)

def basic_calculator(num1: float, num2: float, operator: str) -> Optional[float]:
  """
  Performs addition, subtraction, or multiplication on two numbers.

  Args:
    num1: The first number (float).
    num2: The second number (float).
    operator: A string representing the desired operation ('+', '-', or '*').

  Returns:
    The result of the calculation (float),
    or None if an invalid operator is provided.
  """
  if operator == '+':
    result = num1 + num2
  elif operator == '-':
    result = num1 - num2
  elif operator == '*':
    result = num1 * num2
  else:
    # Handle cases where the operator is not '+', '-', or '*'
    print(f"Error: Invalid operator '{operator}'. Please use '+', '-', or '*'.")
    result = None # Return None to indicate failure
  return {
        "answer": result,
        "message": f"here is the sum of {num1} and {num2} is {result}"
    }


def calculate_sum(x: int, y: int, tool_context: ToolContext):
    """
    Calculates the sum of two integers and returns the result in a dictionary.

    Args:
        x (int): The first integer to add.
        y (int): The second integer to add.
        tool_context (ToolContext): The context object for the tool (not used in this function, but included for ADK tool compatibility).

    Returns:
        dict: A dictionary containing the sum under the key 'answer' and a message string.
    """
    print(f"x: {x}, y: {y}")
    print(f"reulsts: {x + y}")
    return {
        "answer": x + y,
        "message": f"here is the sum of {x} and {y}"
    }
agent = LlmAgent(
    name="qa_assistent",
    model="gemini-2.0-flash",
    instruction="""Yo, wassup, son? It's ya boy from the block, ready to hold you down with whatever you need, word up.
      Holler at me like you would your mans on the stoop — I'm a keep it a buck, no doubt, and drop some real talk.
      If you got somethin' to ask, just spit it, aight? Don't be shy, kid. 🎤 Brooklyn style!

      **When to use tools:**
      - If you need to get bizzy with some numbers, like addin', subtractin', or multiplyin', hit up the `basic_calculator` tool. Just slide in the two numbers and tell it what to do ('+', '-', or '*').
      """,
      tools=[basic_calculator]
)
runner = Runner(
    app_name=APP_NAME,
    agent=agent,
    session_service=session_service,
   
)
async def main():
   while True:
       message = input("Enter a message: ")
       if message.lower() == "exit":
           break
       response = await call_agent_async(runner, USER_ID, SESSION_ID, message)
       print(response)

# Example: Using the query_generation_agent
query_agent = get_query_generation_agent()
query_runner = Runner(
    app_name=APP_NAME,
    agent=query_agent,
    session_service=session_service,
)
async def query_example():
    while True:
        message = input("Enter a natural language request for a query (or 'exit'): ")
        if message.lower() == "exit":
            break
        response = await call_agent_async(query_runner, USER_ID, SESSION_ID, message)
        print("Generated Query:", response)

if __name__ == "__main__":
    asyncio.run(main())




