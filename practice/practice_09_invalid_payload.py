"""
Scenario
--------
Customer: "TypeError: messages must be a list — what does that even mean?"
Focus: Request schema validation and translating Python errors into API guidance.
Debug Path: Mirror the stack trace, show the correct structure, and tie it back
            to the documented `messages: List[ChatCompletionMessageParam]` schema.
"""

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def reproduce_issue() -> None:
    """Builds the payload incorrectly to trigger the TypeError."""
    data = {
        "model": "gpt-4-turbo",
        "messages": "Hello (this should be a list!)",  # Intentional bug.
    }
    openai.ChatCompletion.create(data)


def show_correct_payload() -> None:
    """Use this to demonstrate the fix live."""
    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
    }
    response = client.chat.completions.create( 
        model= "gpt-4-turbo",
        messages= [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ])
    print(response.choices[0].message.content)


if __name__ == "__main__":
    show_correct_payload()
