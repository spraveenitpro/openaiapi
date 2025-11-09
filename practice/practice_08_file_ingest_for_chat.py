"""
Scenario
--------
Customer: "Uploading my CSV so the agent can quote it in chat completions keeps failing."
Focus: File ingestion prerequisites before a chat workflow (Assistants/Responses).
Debug Path: Ensure binary mode when calling `client.files.create`, confirm model
            compatibility, and explain how the uploaded file later feeds chat turns.
"""

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()


def reproduce_issue() -> None:
    """Attempts to upload a file in text mode, mimicking the customer bug."""
    with open("practice/data.csv", "rb") as handle:  # Intentional bug: must be binary.
        uploaded = client.files.create(
            file=handle,
            purpose="assistants",
        )
    print("Uploaded file id:", uploaded.id)


def coaching_notes() -> None:
    """Reference snippet describing the correct approach you can cite verbatim."""
    print(
        "Open the file with open('data.csv', 'rb') before uploading; "
        "Assistants/Responses expect binary streams."
    )


if __name__ == "__main__":
    reproduce_issue()
