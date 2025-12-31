import argparse
import sys

from dotenv import load_dotenv

from aiclient import AiClient
from config import MAX_ITERATIONS


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    load_dotenv()

    ai_client = AiClient(lambda string: print(string))
    args = parser.parse_args()
    prompt = args.user_prompt
    verbose = args.verbose

    if verbose:
        print(f"User prompt: {prompt}")

    if not ai_client.interact(prompt, verbose):
        print(f"Maximum iterations ({MAX_ITERATIONS}) reached")
        sys.exit(1)


if __name__ == "__main__":
    main()
