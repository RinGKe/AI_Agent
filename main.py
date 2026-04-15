import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import *
from functions.call_function import *

parser = argparse.ArgumentParser(prog="AI Agent", description="Chatbot")
parser.add_argument("user_input", type=str, help="User input")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("api_key not found")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_input)])]
    if args.verbose:
        print(f"User prompt: {args.user_input}")

    print("Hello from AI-Agent!")
    print(f"{AGENT_MODEL}")
    print("Thinking...")
    try:
        for _ in range(CALL_LIMIT):
            response = call_agent(client, messages, args.verbose)
            if response:
                print("----------RESPONSE----------")
                print("")
                print(response)
                return
        sys.exit(1)

    except Exception as e:
        print(f"Error calling agent: {e}")


def call_agent(client, messages, verbose=False):
    response = client.models.generate_content(
        model=AGENT_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )
    usage = response.usage_metadata
    if usage == None:
        raise RuntimeError("Failed API request...")

    if response.candidates:
        for c in response.candidates:
            messages.append(c.content)

    if verbose:
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
        print("-----------------------------")

    if not response.function_calls:
        return response.text

    function_results = []
    for function in response.function_calls:
        result = call_function(function, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Error: Empty function response for {function.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_results.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_results))


if __name__ == "__main__":
    main()
