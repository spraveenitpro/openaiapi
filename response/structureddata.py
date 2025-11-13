from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

input_messages = [
    {
        "role": "user",
        "content": "Alice and Bob are going to science fair in new yorkon Friday."
    }
]

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="Extract event information.",
    input= input_messages,
    text={
        "format": {
            "type": "json_schema",
            "name": "calendar_event",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the event"
                    },
                    "date": {
                        "type": "string",
                        "description": "The date of the event"
                    },
                    "location": {
                        "type": "string",
                    },
                    "attendees": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        }
                    }
            },
            "required": ["name", "date", "location", "attendees"],
            "additionalProperties": False,
        },
        "strict": True,
        }
    }
)

print(response.output_text)