"""
Scenario
--------
Customer: "After a few calls I get 429: Rate limit reached."
Focus: Differentiating per-model RPM limits and teaching retry/backoff discipline.
Debug Path: Spot burst loops, implement exponential backoff, and mention
            `Retry-After` plus instrumentation (headers/logging).
"""


from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

load_dotenv()

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6), retry=retry_if_exception_type((RateLimitError)))
def response_with_backoff(client, **kwargs):
    response = client.chat.completions.create(**kwargs)
    print(response.choices[0].message.content)



def reproduce_issue() -> None:
    """Floods the API so you can narrate how rate limiting happens."""
    for i in range(100):  # Intentional bug: no pacing.
        print(f"Sending chat completion #{i}")
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Request number {i}"}],
        )
        time.sleep(0.05)  # Still too aggressive for higher-tier models.


def main():
    client = OpenAI()
    response_with_backoff(client, model="gpt-4o-mini", messages=[{"role": "user", "content": "What is the capital of France?"}])

if __name__ == "__main__":
    main()
