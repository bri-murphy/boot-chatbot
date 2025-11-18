import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import *
from functions.get_files_info import schema_get_files_info
from call_function import available_functions, call_function

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    generate_content(client, messages, verbose)

    
def generate_content(client, messages, verbose):
    for i in range(20):
        try:
            # 1. Call generate_content
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=SYSTEM_PROMPT
                ),
            )
            # 2. Add candidates to messages
            if len(response.candidates) >0:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            # 3. Print verbose info if needed 
            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
            # 4. Check if done (no function calls AND has text)
            if not response.function_calls and response.text !='':
                print("Final response:")
                print(response.text)
                break 
            # 5. If not done: process function calls
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
            # 6. Add function results to messages
            if not function_responses:
                raise Exception("no function responses generated, exiting.")   
            messages.append(types.Content(role="user", parts=function_responses))
        except Exception as e:
            print(f"Error: {e}")
            continue 
    if i == 19:
        print("Chat Limited Reached")
    else:
        print("Chat Ended")


if __name__ == "__main__":
    main()