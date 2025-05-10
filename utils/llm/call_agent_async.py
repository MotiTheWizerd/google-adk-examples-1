from google.genai import types
from colorama import Fore, Back, Style

async def process_agent_response_old(event): 
   print(f"Event ID: {event.id}, Author: {event.author}")

   if event.content and event.content.parts:
      for part in event.content.parts:
         if hasattr(part, "executable_code") and part.executable_code:
            print(f"Debug agent generated code: {part.executable_code}")
         elif hasattr(part, "code_excution_result") and part.code_excution_result:
            print(f"Code execution result: {part.code_excution_result}")
         elif hasattr(part, "tool_response"):
            print(f"Tool response: {part.tool_response}")
          
         elif hasattr(part, "function_response") and part.function_response is not None:
            print(f"Function response: {part.function_response}")
           
        
      if event.is_final_response():
         if(event.content
                and event.content.parts
                and hasattr(event.content.parts[0], "text")
                and event.content.parts[0].text):

                  final_response = event.content.parts[0].text.strip()
                  print(f"{Back.WHITE}{Fore.BLACK}Final response: {final_response}{Style.RESET_ALL}")
                  return final_response
                  
   # Return the event itself for non-final responses to ensure chain continues
   return event

async def process_agent_response(event):
    """
    Logs event details and extracts text if the event is final.
    This function should not cause premature returns from the main event loop.
    """
    print(f"Event ID: {event.id}, Author: {event.author}, Is Final for this event source: {event.is_final_response()}")

    extracted_text = None

    if event.content and event.content.parts:
        for i, part in enumerate(event.content.parts):
            print(f"  Part {i}:")
            if hasattr(part, "text") and part.text:
                print(f"    Text: '{part.text}'")
                # We will rely on event.is_final_response() from the main loop
                # to determine if this text is THE final response of the whole sequence.
                if event.is_final_response():
                     extracted_text = part.text.strip()
            elif hasattr(part, "executable_code") and part.executable_code:
                # In ADK, this might be part.tool_code
                tool_code_attr = getattr(part, "tool_code", getattr(part, "executable_code", None))
                if tool_code_attr:
                    print(f"    Tool Code/Executable Code: {tool_code_attr}")
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                # In ADK, this might be part.tool_response
                tool_response_attr = getattr(part, "tool_response", getattr(part, "code_execution_result", None))
                if tool_response_attr:
                    print(f"    Tool Response/Code Execution Result: {tool_response_attr}")
            elif hasattr(part, "function_response") and part.function_response is not None:
                print(f"    Function response: {part.function_response}")
            # Add any other ADK specific part attributes you need to log

    if extracted_text:
        print(f"{Back.YELLOW}{Fore.BLACK}Text from a final event part: {extracted_text}{Style.RESET_ALL}")
    return extracted_text


async def call_agent_async(runner, user_id, session_id, message):
    """
    Calls the agent asynchronously and waits for the final response of the entire agent execution.
    """
    print(Back.GREEN + f"Calling agent (User: {user_id}, Session: {session_id}) with message: '{message}'" + Style.RESET_ALL)

    # Ensure you are using the correct Content and Part objects expected by your ADK version
    # from google.genai import types or from google.ai.generativelanguage etc.
    new_message_content = types.Content(role="user", parts=[types.Part(text=message)])

    overall_final_response_text = None

    # Run the agent with the message, streaming events as they arrive
    async for event in runner.run_async(user_id=user_id,
                                        session_id=session_id,
                                        new_message=new_message_content): # ADK might use 'request=' or other param name

        print(f"--- Processing Event (ID: {event.id}) ---")
        # Log event details and potentially get text if this event itself is marked final
        text_from_this_event = await process_agent_response(event)

        # The key is to only capture the text as the *overall* final response
        # when the event indicates it's the final one for the whole runner.run_async call.
        # For a SequentialAgent, this means the last agent in the sequence has completed.
        if event.is_final_response():
            if text_from_this_event:
                overall_final_response_text = text_from_this_event
                print(f"{Back.CYAN}{Fore.BLACK}Captured Overall Final Response: {overall_final_response_text}{Style.RESET_ALL}")
            elif event.content and event.content.parts and hasattr(event.content.parts[0], "text") and event.content.parts[0].text:
                # Fallback if log_and_extract didn't pick it up but it's plainly there
                overall_final_response_text = event.content.parts[0].text.strip()
                print(f"{Back.CYAN}{Fore.BLACK}Captured Overall Final Response (fallback): {overall_final_response_text}{Style.RESET_ALL}")
            else:
                # This might happen if the final event is just a marker without text,
                # or if the text was in a previous event that wasn't THE final one.
                # Or, if the final output is structured data not in a simple text part.
                print(f"{Back.RED}Final event (ID: {event.id}) received, but no straightforward text found in its parts for the overall response. The actual final data might have been in an earlier event if the agent produces complex output before signaling completion.{Style.RESET_ALL}")


    # The loop has completed, meaning the runner.run_async has finished.
    # overall_final_response_text should now hold the final text from the SequentialAgent.
    if overall_final_response_text:
        return overall_final_response_text
    else:
        # This case means the runner finished, but we didn't identify a clear final text response.
        # This could happen if the last agent doesn't produce simple text or if there was an issue.
        print(Back.RED + "Agent execution finished, but no clear overall final text response was captured." + Style.RESET_ALL)
        return "Agent finished, but no final textual response was extracted."
