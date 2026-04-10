import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import *
from functions.call_function import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api_key not found")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(prog="AI Agent", description="Chatbot")
parser.add_argument("user_input", type=str, help="User input")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_input)])]


def main():
    print("Hello from AI-Agent!")
    print("Thinking...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    usage = response.usage_metadata
    if usage == None:
        raise RuntimeError("Failed API request...")

    if args.verbose:
        print(f"User prompt: {args.user_input}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
        print("------------------------------")
    if response.function_calls:
        for f in response.function_calls:
            print(f"Calling function: {f.name}({f.args})")
    print("-----------RESPONSE-----------")
    print(response.text)


if __name__ == "__main__":
    main()
