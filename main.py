import os

from google import genai
from functions.call_function import call_function, available_functions
from google.genai import types
from dotenv import load_dotenv
import argparse
import sys
from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Generate content using Gemini AI")
    parser.add_argument("content", help="The content to process")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    verbose = args.verbose
    user_prompt = args.content


    if len(sys.argv) < 2:
        print("Usage: python main.py <content>")
        sys.exit(1)
    user_prompt = sys.argv[1]
    if not user_prompt:
        print("Content cannot be empty.")
        sys.exit(1)
    if len(user_prompt) > 4096:
        print("Content exceeds the maximum length of 4096 characters.")
        sys.exit(1)
        

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

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

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    
if __name__ == "__main__":
    main()