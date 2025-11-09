"""
Scenario
--------
Customer: "It says: model does not support this feature."
Focus: Mapping product capabilities (vision, JSON mode, function calling) to models.
Debug Path: Inspect payload, confirm which model versions support the requested
            feature, and suggest the closest compatible alternative.
"""

from openai import OpenAI, BadRequestError
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()


def reproduce_issue() -> None:
    """Uses a legacy chat model with a multimodal payload to trigger an error."""
    try:
        response = client.chat.completions.create(
            #model="gpt-3-5-turbo",  # Intentional bug: no image understanding support.
            model="gpt-4o",  # Intentional bug: no image understanding support.
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this chart."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg"
                            },
                        },
                    ],
                }
            ],
        )
        print(response.choices[0].message.content)
    except BadRequestError as exc:
        print("Caught BadRequestError:", exc)
        print("Coach Tip: switch to gpt-4o or gpt-4.1 for multimodal chat payloads.")


if __name__ == "__main__":
    reproduce_issue()
