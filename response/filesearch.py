from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

input_messages = [
    {
        "role": "user",
        "content": "Hi There!"
    }
]

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="You are a helpful assistant.",
    input= input_messages,
)

print(response.output_text)

