"""
Scenario
--------
Customer: "I keep getting 401 Unauthorized: Incorrect API key provided."
Focus: Environment configuration, secret hygiene, and verifying the active key.
Debug Path: Confirm `OPENAI_API_KEY` presence, rotate credentials if needed,
            and highlight differences between `os.environ` and literal strings.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def reproduce_issue() -> None:
    """Shows the failure caused by a hard-coded, invalid API key."""
    openai.api_key = "sk-wrongkey"  # Intentional bug: this key is invalid/old.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello from the interview prep script."}],
    )
    print(response)


def recommended_fix() -> None:
    """Example remediation that mirrors what you should coach the customer to do."""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "What is the capital of France?"}],
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    recommended_fix() 
