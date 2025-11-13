from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from typing import List

load_dotenv(override=True)
# Create a Pydantic model for the calendar event

class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name:str
    date:str
    location:str
    attendees:List[str]

schema = Event.model_json_schema()
print(schema)

client = OpenAI()

input_messages = [
    {
        "role": "user",
        "content": [{
            "type": "input_text",
            "text": "Alice and Bob are going to science fair in new york on Friday."
        }]
    }
]

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="Extract event information.",
    input= input_messages,
    text={
        "format": {
            "type": "json_schema",
            "name": "event_info",
            "schema": schema,
            "strict": True,
        }
    }
)

print(response.output_text)