import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
import sys


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


    model = "gemini-2.0-flash-001"

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

    response = client.models.generate_content(
        model=model,
        contents=messages,
    )
    if verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)


if __name__ == "__main__":
    main()