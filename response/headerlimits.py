import time

from openai import OpenAI, AuthenticationError, RateLimitError
from dotenv import load_dotenv
load_dotenv(override=True)

client = OpenAI()

def safe_request(prompt):
    try:
        # Make a simple API call (Responses API example)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        print("Response ID:", response.id)
        print("Model:", response.model)
        print("Created:", response.created_at)
        print("Status:", response.status)
        print("Input tokens:", response.usage.input_tokens)
        print("Output tokens:", response.usage.output_tokens)
        print("Total tokens:", response.usage.total_tokens)
        print("Assistant output:\n", response.output[0].content[0].text)
        
        # headers = response.response_headers

        # for key, value in headers.items():
        #     if key.startswith("x-ratelimit"):
        #         print(f"{key}: {value}")
        
        print(response.model_dump_json(indent=2))




    except RateLimitError as e:
        print("⚠️ Hit rate limit! Waiting 60 seconds...")
        time.sleep(60)
    except Exception as e:
        print(f"Unexpected error: {e}")

      


# Example usage
safe_request("Write a 3-line poem about computers dreaming.")
