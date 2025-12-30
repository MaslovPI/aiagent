import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Api key for AI provider is not found")
    client = genai.Client(api_key=api_key)

    args = parser.parse_args()
    prompt = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("API request has failed, metadata is empty")

    tokens_prompt = response.usage_metadata.prompt_token_count
    tokens_response = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {tokens_prompt}")
        print(f"Response tokens: {tokens_response}")
    print("Response:")
    if response.function_calls is None:
        print(response.text)
    else:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()
