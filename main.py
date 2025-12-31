import argparse
from dotenv import load_dotenv
from aiclient import AiClient
from call_function import call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    load_dotenv()

    ai_client = AiClient(lambda string: print(string))
    args = parser.parse_args()
    prompt = args.user_prompt
    verbose = args.verbose
    ai_client.interact(prompt, verbose)


if __name__ == "__main__":
    main()
