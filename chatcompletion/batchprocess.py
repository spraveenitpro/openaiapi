
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic import BaseModel

client = OpenAI()

# Define the Pydantic model for the structured output
class StoryResponse(BaseModel):
    stories: list[str]
    story_count: int

num_stories = 10
content = "Once upon a time,"

prompt_lines = [f"Story #{i+1}: {content}" for i in range(num_stories)]
prompt_text = "\n".join(prompt_lines)

messages = [
    {
        "role": "developer",
        "content": "You are a helpful assistant. Please respond to each prompt as a separate short story."
    },
    {
        "role": "user",
        "content": prompt_text
    }
]

# batched example, with all story completions in one request and using structured outputs
response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=messages,
    response_format=StoryResponse,
)

print(response.choices[0].message.content)