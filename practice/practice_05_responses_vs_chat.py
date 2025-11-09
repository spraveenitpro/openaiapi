"""
Scenario
--------
Customer: "Why does this raise KeyError: 'choices'?"
Focus: Clarifying differences between `chat.completions` and `responses.create`.
Debug Path: Ask why they switched APIs, show correct attribute access, and
            optionally guide migration back to `chat.completions.create`.
"""

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()


def reproduce_issue() -> None:
    """Uses the Responses API but still tries to read Chat Completion fields."""
    response = client.responses.create(
        model="gpt-4-turbo",
        input=[{"role": "user", "content": "Write a haiku about whales."}],
    )
    print(response["choices"][0]["message"]["content"])  # Intentional KeyError.


def show_correct_usage() -> None:
    """Reference snippet you can mention to unblock the customer."""
    response = client.responses.create(
        model="gpt-4-turbo",
        input=[{"role": "user", "content": "Write a haiku about whales."}],
    )
    print("output_text:", response.output_text)


if __name__ == "__main__":
    show_correct_usage()
