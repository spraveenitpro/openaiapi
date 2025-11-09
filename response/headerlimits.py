import time
from openai import OpenAI, AuthenticationError, RateLimitError
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

def safe_request(prompt):
    try:
        raw_response = client.responses.with_raw_response.create(
            model="gpt-4o-mini",
            input=prompt
        )

        response = raw_response.parse()

        print("Response ID:", response.id)
        print("Model:", response.model)
        print("Created:", response.created_at)
        print("Status:", response.status)
        print("Input tokens:", response.usage.input_tokens)
        print("Output tokens:", response.usage.output_tokens)
        print("Total tokens:", response.usage.total_tokens)
        print("Assistant output:\n", response.output[0].content[0].text)

        # Access rate limit headers from raw_response
        print("\n📊 Rate Limit Headers:")
        print(f"x-ratelimit-limit-requests: {raw_response.headers.get('x-ratelimit-limit-requests')}")
        print(f"x-ratelimit-limit-tokens: {raw_response.headers.get('x-ratelimit-limit-tokens')}")
        print(f"x-ratelimit-remaining-requests: {raw_response.headers.get('x-ratelimit-remaining-requests')}")
        print(f"x-ratelimit-remaining-tokens: {raw_response.headers.get('x-ratelimit-remaining-tokens')}")
        print(f"x-ratelimit-reset-requests: {raw_response.headers.get('x-ratelimit-reset-requests')}")
        print(f"x-ratelimit-reset-tokens: {raw_response.headers.get('x-ratelimit-reset-tokens')}")


    except RateLimitError:
        print("⚠️ Hit rate limit! Waiting 60 seconds...")
        time.sleep(60)

    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
safe_request("Write a 3-line poem about computers dreaming.")
