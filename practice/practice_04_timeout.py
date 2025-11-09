"""
Scenario
--------
Customer: "Every request times out instantly!"
Focus: Balancing timeout settings with workload size and network latency.
Debug Path: Inspect client initialization, confirm network health, adjust timeout
            for long-form generations, and consider retries for transient failures.
"""

from openai import APITimeoutError, OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(timeout=500)  # Intentional bug: virtually guarantees a timeout.


def reproduce_issue() -> None:
    """Requests a long response with an unrealistically low timeout value."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Generate a 100 -word essay about resilience in the face of adversity.",
                }
            ],
        )
        print(response.choices[0].message.content)
    except APITimeoutError as exc:
        print("Caught APITimeoutError:", exc)
        print("Coaching Tip: set timeout to several seconds, not 100ms.")


if __name__ == "__main__":
    reproduce_issue()
