import os

from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


class AiClient:
    def __init__(self, log) -> None:
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key is None:
            raise RuntimeError("Api key for AI provider is not found")
        self.client = genai.Client(api_key=self.api_key)
        self.log = log

    def __prompt_for_response__(self, prompt):
        messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
        return self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

    def interact(self, prompt, verbose):
        response = self.__prompt_for_response__(prompt)

        if response.usage_metadata is None:
            raise RuntimeError("API request has failed, metadata is empty")

        tokens_prompt = response.usage_metadata.prompt_token_count
        tokens_response = response.usage_metadata.candidates_token_count

        if verbose:
            self.log(f"User prompt: {prompt}")
            self.log(f"Prompt tokens: {tokens_prompt}")
            self.log(f"Response tokens: {tokens_response}")
        self.log("Response:")
        if response.function_calls is None:
            self.log(response.text)

        if response.function_calls is None:
            self.log(response.text)
        else:
            results = []
            for function_call in response.function_calls:
                call_result = call_function(function_call, verbose)
                if call_result.parts is None or len(call_result.parts) == 0:
                    raise Exception("Call result content parts are empty")
                response = call_result.parts[0].function_response
                if response is None:
                    raise Exception("Expected response, got none")
                actual_result = response.response
                if actual_result is None:
                    raise Exception("Actual result of the function call is None")
                results.append(actual_result)
                if verbose:
                    self.log(f"-> {actual_result}")
