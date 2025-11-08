import time
import openai
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def safe_request(prompt):
    try:
        # Make a simple API call (Responses API example)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        # Print the response text
        print(response.output_text)

        # Access raw response headers via the response.response_headers property
        headers = response.response_headers
        print("\n--- Rate Limit Headers ---")
        for key, value in headers.items():
            if key.startswith("x-ratelimit"):
                print(f"{key}: {value}")

        # Optionally, handle rate-limit logic
        remaining_requests = int(headers.get("x-ratelimit-remaining-requests", 1))
        reset_requests = headers.get("x-ratelimit-reset-requests", "0s")

        if remaining_requests == 0:
            # Convert reset time (e.g., "60s") to seconds
            reset_seconds = int(''.join(filter(str.isdigit, reset_requests)))
            print(f"\n🔁 Rate limit reached. Sleeping for {reset_seconds} seconds...")
            time.sleep(reset_seconds)

    except openai.RateLimitError:
        print("⚠️ Hit rate limit! Waiting 60 seconds...")
        time.sleep(60)
    except Exception as e:
        print(f"Unexpected error: {e}")


# Example usage
safe_request("Write a 3-line poem about computers dreaming.")
