"""
Scenario
--------
Customer: "I get a 400 error when sending chat completions."
Focus: Schema validation, required fields, reading error payloads.
Debug Path: Check the request body, ensure `model` is supplied, and reinforce
            how to map error messages back to specific parameters.
"""

from openai import OpenAI, BadRequestError
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()


def reproduce_issue() -> None:
    """Omits the required model parameter to trigger a TypeError (client-side validation)."""
    try:
        client.chat.completions.create(
            messages=[{"role": "user", "content": "Hi from missing-model script."}]
        )
    except TypeError as exc:
        print("Caught TypeError:", exc)
        print("Note: The OpenAI SDK validates required parameters before making the API call.")
        print("Reminder: include model='gpt-4-turbo' (or similar) in the payload.")
    except BadRequestError as exc:
        print("Caught BadRequestError:", exc)
        print("Reminder: include model='gpt-4-turbo' (or similar) in the payload.")



def resolved_issue() -> None:
    try:
        response = client.chat.completions.create(
            model="o3",
            messages=[{"role": "user", "content": "what is the capital of france?"}],
            temperature=0.7
        )
        print(response.choices[0].message.content)
    except BadRequestError as e:
        print("Caught BadRequestError:", e)
        print("Reminder: include model='gpt-4o-mini' (or similar) in the payload.")
    except Exception as e:
        print("Caught Exception:", e)
        print("Reminder: include model='gpt-4o-mini' (or similar) in the payload.")

if __name__ == "__main__":
    resolved_issue()
